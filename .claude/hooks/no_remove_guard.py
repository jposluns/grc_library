#!/usr/bin/env python3
"""no-remove-guard: a Claude Code PreToolUse hook for the Bash tool that denies file removal.

BEST EFFORT (round 56). This is a command-text guard: it decides from the text of a shell command alone,
and the grammar it reads is open (bash itself, every program a command starts, and the settings,
aliases, functions and files those read can each change what the same text runs). It is a best-effort
first layer against accidental removal. It cannot stop deliberate evasion, and every review round has
found more forms that pass it (RESIDUAL names those known). Put it in front of protection that does not
read shell text: files that are read-only to the session (permissions, ACLs, a read-only mount) or
recoverable (version control that holds every change, snapshots, backups).

PURPOSE AND LIMIT. This guard targets ACCIDENTAL removal: an orchestrator that removes files by mistake in
a bash command. It models bash only (up to the bash 5.3 constructs it names). Deliberate obfuscation, and
other shells (zsh, dash, sh, fish and the like, which parse the same text differently), are a named
residual (see RESIDUAL): a command-text guard cannot promise to stop deliberate evasion. A bash, sh, dash,
zsh, ksh, ksh93, mksh, ash, fish, tcsh or csh -c string, and a su -c string, is checked with this bash
grammar too. File permissions are the real boundary.

Standard library only; it imports nothing from the repository and runs as python3 -I <path>.

SCOPE. This guard is for the grc orchestrator's MAIN session only. It is not for workers: workers are
bounded by their own run scratch, account permissions and ACLs, and this hook is not part of their policy.
In the main session it denies a Bash command that removes files and points at the set-aside folders
/tmp/grc/deleteme and /tmp/deleteme-grc, where the session moves what it wants gone so that a human makes
the deletion (round 37: its deny message advises mv --backup=numbered, since a plain mv into the
folder can overwrite an earlier discard of the same name; by GNU mv's documentation, not witnessed,
--backup=numbered first renames that earlier discard to NAME.~N~. Round 38, qanorm37 F2: it no longer
advises mv -n, which, when the name already exists in the folder, does not move the path at all and
leaves it where it was, possibly without a message, so the session may wrongly believe it set the path
aside; also by GNU mv's documentation, not witnessed). It has no in-band opt-out: no environment variable, marker, comment or flag in the command
turns it off.

REGISTRATION. Add it to a settings file that the grc main session loads and the workers do not, with an
absolute path to this file:

    {"hooks": {"PreToolUse": [{"matcher": "Bash",
                               "hooks": [{"type": "command",
                                          "command": "python3 -I /absolute/path/to/no_remove_guard.py",
                                          "timeout": 10}]}]}}

Round 37 (grc round 36 MEDIUM): the file's name is no_remove_guard.py, with underscores (it was developed
as draft-offpath/norm1/no_remove_guard.py; round 52, grc review of round 50, words that path as history,
so that this sentence holds wherever the file is installed). Its earlier name, no-remove-guard.py, holds the word remove at a hyphen boundary, so once the guard was
registered under that name the broad layer refused every command that named the file (its --self-test,
sha256sum, git add, git diff, git commit); the removal-word test is unchanged, and the self-test holds
allow rows for those five commands on this name. Keep the underscores if you copy or rename the file.
Round 48 (grc review of round 47) adds an allow row that runs both layers on sha256sum of the path of
the file actually running, so a copy or rename by an installer whose path holds a word the broad layer
refuses fails the self-test where it is installed. Round 49 (grc review of round 48): that row takes the
path as the self-test was started with it (os.path.abspath(__file__)), not the resolved real path
(os.path.realpath(__file__)), which followed a symlink installed under a refused name to its allowed
target, so the row passed there. Round 51 (grc review of round 50) corrects round 50's reason for
abspath: since Python 3.9 the main script's __file__ is already absolute, so a relative start (python3 -I
no_remove_guard.py --self-test) needs no abspath (witnessed at round 51 with python3 3.14.4 on the review
host: a script started by a relative path, by a relative path through a symlink, or loaded by importlib
from a relative path had an absolute __file__). The reason that still holds is the symlinked install:
abspath, unlike realpath, resolves no symlink, so the row tests the name the self-test was started by
(the symlink start above kept the link's name). abspath stays as a no-op guard for a loader or a Python
before 3.9 that leaves __file__ relative (not witnessed). A broad row builds the same sha256sum command
on the earlier name no-remove-guard.py in the same directory (the directory from os.path.abspath(__file__),
as in the allow row) and requires the broad refusal; it shows only that the broad layer refuses that
command text, and that the own-path allow row would then fail its pin check is inference (round 51
rewords round 50, which said the check is shown to fail). Run the self-test by the path you register.

Before you register it, confirm that the grc main session's Bash tool runs its commands in bash: this
guard models bash only (see PURPOSE).

Run python3 -I <path> --self-test to check it in place before relying on it.

WHAT IT DENIES. It reads the hook JSON on stdin and lexes the command (quotes, escapes, comments,
here-documents, command and process substitution, parameter and arithmetic expansion, including the
(( ... )) command, the for (( ... )) header and $[ ... ]), then walks every command position in every
segment of the compound command: pipelines, ;, &, &&, ||, newlines, subshells, brace groups, if, while,
until, for, select, case, function bodies, the body of each command substitution, process substitution,
backquote and unquoted here-document substitution, and the action string of trap. In command position it
denies:
  * rm, rmdir, unlink, shred, srm, wipe, including a quoted or escaped spelling ('rm', \\rm, $'\\x72m')
    and any path whose last component is one of them (/bin/rm, /usr/bin/rm), but not one whose only
    argument is --help or --version (the inner layer allows rm --help; the broad layer below refuses it,
    as its text holds rm: round 37);
  * find with -delete, or with -exec, -execdir, -ok or -okdir whose command is itself a removal; fd or
    fdfind with any -x, --exec, -X or --exec-batch whose command is a removal; gio remove;
  * git rm given -f or --force (also in a cluster such as -rf, or abbreviated as --f to --forc) and no
    --cached, after the git options it knows (-C, -c, --git-dir, --work-tree and the like): git rm -f
    deletes a file even when it holds changes that no commit holds (git rm without -f: see RESIDUAL);
  * after the same git options: git clean, except a dry run (-n or --dry-run, or an abbreviation that
    git accepts, --d to --dry-ru, with no later --no- option and no expansion before --) and git clean
    -h or --help alone; git worktree remove with -f or --force; git reset --hard (or --h to --har); git
    stash, git stash push or git stash save with -u, --include-untracked, -a or --all (round 48: not git
    stash drop or git stash clear, nor git gc --prune=now, git sparse-checkout set, or git apply, git am
    or patch given a diff that deletes a file; see RESIDUAL, the round 48 item); git checkout with
    -f or --force (--f to --forc) of a path: one named after --, given by --pathspec-from-file, a second
    operand after the tree-ish (git checkout -f main x), any operand with --theirs or --ours (also -3
    and -2, or --th and --ou abbreviated; round 20), an operand that cannot be a branch name (.,
    a word that starts with . or /, ends with /, or holds /. or //, or holds *, ? or [, which git reads
    as a pathspec glob), or an operand built at run time (a glob, a brace expansion or an expansion such
    as "$F", which may be or become a path or several); git checkout -f or --force with no operand; git
    switch with -f, --force or --discard-changes (or an abbreviation of either); and (round 18) git
    submodule deinit -f or --force, git read-tree with both -u and --reset, and git checkout-index -f or
    --force (an expansion before -- that may become the option denies as cannot-parse); (round 30,
    qanorm29 F1) git submodule update -f or --force, with or without --checkout, read as deinit is (by
    git's documentation, inferred and not witnessed, it throws away local changes in submodule working
    trees; also in the text tests for round 15 forms, and an expansion before -- denies as cannot-parse,
    so git submodule update --init "$path" is an over-deny: write git submodule update --init -- "$path");
    and (round 31, qanorm30 MINOR-1) git rebase --abort or --skip and git am --abort (each also as an
    abbreviation), read as git reset --hard is (by git's documentation, inferred and not witnessed, each
    resets working-tree files to a commit, so it can throw away local changes to tracked files; also in
    the text tests for round 15 forms, and, as for git reset --hard, an expansion is not read: see RESIDUAL);
    and (round 37) git merge --abort and git cherry-pick --abort, each also as an abbreviation, read the
    same way; and (round 38, qanorm37 F1) git am --skip, git cherry-pick --skip, git revert --abort and
    git revert --skip, each also as an abbreviation, read the same way, so that every --abort and --skip
    of rebase, am, merge, cherry-pick and revert is denied (the derivation from git's option lists is at
    GIT_ABANDON_OPTIONS; their --quit stays allowed: see RESIDUAL); and (round 39, qanorm38 F1) git
    checkout and git restore with -m, --merge, --conflict, --ours, --theirs, -2 or -3 (each also as an
    abbreviation or in a short-option cluster) of a named path: for git checkout a path is named as for
    -f above, or by any operand, so git checkout -m WORD is denied though WORD may be a branch (an
    over-deny of a branch switch; git switch -m BRANCH stays allowed; round 40, qanorm39 F4: so are git
    checkout --merge main and --conflict=diff3 main, git checkout -m -b new origin/main, a branch created
    with a merge from a start point, and git checkout --ours, --theirs, -2 and -3 with no operand, which
    git refuses to run; and, reading an abbreviation of several long options as all of them, a command
    git refuses as ambiguous, such as git checkout --o x and git restore --o x); for git restore every
    operand is a path. Each rewrites a conflicted path from the
    index stages and overwrites a conflict resolution made by hand (witnessed, git 2.53.0; the
    derivation from git's option lists is at GIT_STAGE_REWRITE_OPTIONS); (round 40, qanorm39 F1) every
    long option of both commands is read through one table, GIT_PATH_COMMAND_LONGS, so each abbreviation
    git accepts counts as the option (git checkout -m --pathspec-fr=list); (qanorm39 F2) behind xargs,
    which appends the items it reads as operands, git checkout or git restore with such an option and no
    path named (git diff --name-only | xargs git restore --theirs, xargs git checkout -m); (round 41,
    qanorm40 N1, N8) the same behind every program the guard reads that puts the paths it finds or reads
    into the command it runs: gxargs, fd and fdfind -x, -X,
    --exec and --exec-batch (fd -e c -X git restore --theirs), find -exec, -execdir, -ok and -okdir, and
    GNU parallel, sem, xe and rush (ls | parallel git checkout -m); (round 45, qanorm44 F1 and F2,
    replacing the round 43 and round 44 rules there, which read git's options to find the subcommand)
    behind each of those programs (find, gfind and bfs only in a block that holds {}), with any wrapper
    before git (from round 46 the wrapper itself is cannot-parse there, see below), as cannot-parse
    whatever the program's options, every git command except one whose word
    right after git is a plain literal word (no quote, backslash, expansion, glob or brace) naming one of
    the read-only subcommands log, show, diff, status, ls-files, ls-tree, blame, cat-file, rev-parse,
    rev-list, shortlog and check-ignore (_GIT_APPENDED_ALLOWED, where each has its reason). So these are
    cannot-parse: any git option before the subcommand (ls | xargs git -C repo restore --ours, ls | xargs
    git '--namespace=x log' restore --ours); any subcommand outside the list (ls | xargs git restore,
    ls | xargs git add, an alias such as ls | xargs git co --ours); no subcommand, so the items the
    program reads supply it ((echo restore; echo --ours) | xargs git); a replacement string or an
    input-source separator in its place (parallel git {} --ours f ::: restore, parallel git :::: subs.txt);
    an expansion in its place (xargs git $SUB); a git word that is one piece of a quoted shell line split
    at blanks and shell operators, or that holds a quote or a backslash (ls | parallel 'git log {}', ls |
    xe 'git restore --ours'); a git command after any program option that may name a replacement string,
    whatever its value (a short-option cluster holding I, J or i, as in xargs -I{}, -0IR or -i; a long
    option that abbreviates --replace, --rpl, --parens or a *replace option of GNU parallel), or after an
    expansion (xargs $OPTS git log); and an expansion, which may be git, followed anywhere later by a
    subcommand git ships that is not in the list (xargs $GIT restore --ours) (_appended_git_check);
    (round 46, qanorm45 F1, F2, F4, one level up from round 45) behind each of those programs, as
    cannot-parse, every command whose first word is not exactly one of the plain programs that run no
    command they are given (round 47, qanorm46 m2: diff -l and --paginate run the fixed program pr,
    which runs nothing it is given) (_APPENDED_PLAIN_PROGRAMS: cat, head, tail, wc, ls, stat, du, grep,
    egrep, fgrep, echo,
    printf, basename, dirname, realpath, readlink, the md5sum to b2sum and cksum checksums, cut, uniq,
    nl, od, cmp, diff, touch, chmod, mkdir, cp, mv, ln, and git under the rule above), written as a plain
    literal word with no path, quote, backslash, expansion, assignment word or replacement string; so
    env (env -S'git restore --ours' and --split-string included), sudo, nice, nohup, time, timeout,
    stdbuf, flock, xargs, sh, bash and any other program that runs a command it is given are
    cannot-parse there (ls | xargs env -S'git restore --ours', fd -e c -X env '-Sgit checkout -m', ls |
    xargs sudo env '-Sgit restore --ours'), and so is a replacement string or {} as the command word
    (echo git | xargs -I% % restore --ours f, echo t | parallel gi{} restore --ours f, find /usr/bin
    -name git -exec {} restore --ours f ';'); a listed name that a replacement option before it may
    rewrite (xargs -I gr grep, xargs -Igr grep), or with an expansion before it; behind GNU parallel,
    sem, xe and rush, an option the PATH_APPENDERS table does not settle, one that names a program, perl
    code or a profile (--ssh, --compress-program, --decompress-program, --filter, --group-by, --profile,
    --sshloginfile, -J, xe -s; round 47, qanorm46 m1: not --limit, which also runs a command it names,
    see RESIDUAL), an option value that holds a blank or {=, a literal {= anywhere in the command (a
    perl expression in the default {= =} delimiters; round 47, qanorm46 M2: not one in delimiters that
    --parens sets, see RESIDUAL) or an expansion in the command, and a later command in the shell line
    they build whose first word is not listed (ls | parallel grep x '{};' env ...; round 47, qanorm46
    B1: not a command after a + of xe -p pattern mode, see RESIDUAL); a GNU parallel or sem long option
    in any letter case (parallel --Replace=log git log --ours f); xargs or gxargs options the WRAPPERS
    table does not settle; no command word behind GNU parallel, sem, xe or rush (the items are the
    commands); and, whenever such a command is checked, any variable assignment anywhere in the same
    command text that names, written out as a literal name, a setting such a program reads (round 47,
    qanorm46 M1, B2: not a name built from a variable or by export $(...), and not a BASH_FUNC_ name;
    see RESIDUAL) (_APPENDED_SETTING: PARALLEL and every PARALLEL_ name, every GIT_ name, PATH,
    SHELL, BASH_ENV, ENV, HOME, XDG_CONFIG_HOME, LD_ names, PAGER, LESS names, EDITOR and VISUAL, as NAME=,
    NAME+= or a whole word such as export NAME), as in echo restore | PARALLEL='-I log' parallel git log
    --ours f, export PARALLEL='-I log'; echo restore | parallel git log --ours f and ls | xargs env
    GIT_EXTERNAL_DIFF=./fix.sh git diff (_appended_command_check);
    (qanorm39 F3) git checkout and git
    restore of a named path from a tree that is MERGE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD, REBASE_HEAD or
    AUTO_MERGE (git checkout MERGE_HEAD -- f, git restore -s MERGE_HEAD f), refs a merge, cherry-pick,
    revert or rebase writes while it is in progress, and (round 41, qanorm40 N4) FETCH_HEAD, the
    main-worktree/ and worktrees/NAME/ spellings of each, any letter case, and the ref in any operand
    position of git checkout before -- (git checkout $OPT MERGE_HEAD -- f); (qanorm40 N7) a word after
    --end-of-options is an operand (git restore --ours --end-of-options -weird); (round 42, qanorm41 F1)
    fd's exec word attached or after a value option (fd --exec=git restore --theirs) is read as an exec
    word; (qanorm41 F2) an operation ref counts only
    as the whole word, with a revision suffix (MERGE_HEAD~1, MERGE_HEAD:dir) or (round 43, qanorm42 N2)
    on the left of the merge-base form A...B (git checkout MERGE_HEAD...HEAD -- f), not as the start of a
    file or branch name (auto_merge.py); (qanorm41 F3) find -exec, -execdir, -ok and -okdir append a path
    only to a block that holds {}; (qanorm41 F5) gfind and bfs are read as find (bfs -rm as -delete);
  * after the same git options, a git subcommand that runs a command whose command holds a removal
    form, checked as a shell command string: git submodule foreach (also --recursive), git rebase
    --exec, --exec=, -x (also in a cluster such as -ix), git bisect run, git filter-branch --tree-filter,
    --index-filter and its other filters, git difftool -x or --extcmd, --upload-pack of git clone (-u),
    fetch, pull and ls-remote, --exec of git archive and ls-remote, --receive-pack and --exec of git
    push, the --sendmail-cmd, --to-cmd, --cc-cmd and --header-cmd of git send-email, and git grep -O or
    --open-files-in-pager with an attached pager (each long option also as an abbreviation);
  * the -c string of bash, sh, dash, zsh, ksh, ksh93, mksh, ash (also busybox ash), fish (also fish
    --command, -C and --init-command, attached or in a cluster such as -iC, each wherever it appears among
    fish's words), tcsh or csh (-c alone or in a cluster such as -ec, after their
    options), and of su (-c, --command or --session-command, before or after the user name), checked as a
    command to any depth, so find -exec sh -c 'rm "$1"' _ {} \\; is denied too; a string it cannot
    parse, and an expansion that may become -c or the string, deny as cannot-parse when a removal word,
    or a round 15 removal form (git clean, git reset --hard, git stash -u or -a, git checkout or switch
    -f, cargo clean, rsync --delete; see _removal_form_in), is in the text;
  * a perl -e or -E program (attached, separate or after a cluster such as -le) that holds the word
    unlink or rmtree, or that names system, exec, qx or readpipe or holds a backquote (a shell command)
    and also holds a removal word or a round 15 removal form; rsync with --delete, --del, any --delete-*
    option, --remove-source-files or --remove-sent-files, or (round 23) an abbreviation of one of them
    from --dele or --remov on (--delet, --remov; rsync accepts an unambiguous prefix); cargo clean
    after the cargo options it knows
    (and +toolchain), unless its only argument is -h or --help;
  * any of the above behind command, builtin, busybox, exec, env (its options, -S split strings and
    NAME=VALUE assignments), sudo, doas, nohup, nice, ionice, timeout, time, stdbuf, xargs, setsid,
    flock (flock FILE COMMAND, and flock FILE -c STRING, checked as a command string), taskset (MASK
    COMMAND; taskset -p runs nothing), chrt ([PRIORITY] COMMAND; chrt -p and -m run nothing), unshare,
    fakeroot, eatmydata, strace, ltrace, uv run (after the uv options it knows), pipx run or poetry run
    (after the pipx or poetry options it knows; pipx run checks the app name as a command word), and the
    bash builtin jobs given -x (jobs -x COMMAND runs COMMAND), nested to any depth (past 32 levels of
    nesting it no longer reads the argv, and denies as cannot-parse when the argv holds a removal word or
    a round 15 removal form); (round 21) a long option of these wrappers and runners is also read in each
    unambiguous abbreviation that getopt_long accepts (timeout --kill=1, sudo --us, env --un, nice --adj);
    one that abbreviates several options that all take a value, or all take none, is read as that kind,
    and one that abbreviates both kinds stays an option it does not know;
  * a command word it has no rule for (not one above, and not a bash builtin that never runs an operand,
    such as echo, printf, test, cd or export) with a later unquoted word of its argv that is a removal
    command name (rm, rmdir, unlink, shred, srm, wipe, also as a path such as /bin/rm), or git followed
    by a removal subcommand form (one the git rules above deny or count as cannot-parse), or (round 23)
    cargo or rsync followed by a form the cargo or rsync rule above denies (chroot /srv cargo clean,
    mywrap rsync -a --delete a b), or (round 20)
    a later unquoted word that names a shell, su, an interpreter (python, perl, awk, sed), find or fd,
    ssh, eval or a wrapper or runner it knows, from which the full argv check finds a removal or a form
    it cannot read (chroot /srv sh -c 'rm -rf x', watch find . -delete): denied as cannot-parse, because
    that command word may be a wrapper the guard does not know (chroot DIR rm x, watch rm x); see
    FAIL-SAFE for the over-deny this adds;
  * (round 20) ssh with a remote command, checked as a shell command string (its words joined with
    spaces); an awk program that calls system() or pipes to or from a command string, and a sed script
    with the e command or the s///e flag (not with --sandbox), that hold a removal word or a round 15
    removal form, as cannot-parse; (round 21) for such an awk program (system(), a pipe, or getline from
    a command), its -v and --assign values, the operands after it and the NAME=VALUE words before awk
    (also those env or sudo passes on), which it reads as variables, ARGV or ENVIRON, count as its text
    (awk -v c='rm x' 'BEGIN{system(c)}', C='rm x' awk 'BEGIN{system(ENVIRON["C"])}');
  * (round 21) after the same git options, a git command that sets help.autocorrect (-c or
    --config-env help.autocorrect=..., any letter case, or git config naming it), whatever its
    subcommand, and a subcommand that git does not ship (an alias, a git-WORD program, or a mistyped
    subcommand that autocorrect may run as another) whose git argv holds a removal word or a round 15
    removal form, as cannot-parse;
  * a literal python, python3, ipython, pypy or py (the python launcher) -c program (a version, a t or
    d suffix and -dbg included, such as python3.13t or python3-dbg) that, parsed with ast, refers to
    os.remove, os.unlink, os.rmdir, os.removedirs, shutil.rmtree, or the unlink or rmdir method (pathlib Path.unlink and
    Path.rmdir), including through an import alias, from-import, star import or getattr with a literal
    name (getattr(X, "remove") only when X is an os module, as for X.remove), or (round 23) through a
    plain name an assignment binds to an os module (o = os; o.remove('x'), o = __import__('os'),
    (o := os), o, p = os, 1, and a chain of such names), or (round 24) through an expression whose
    value is an os module: a walrus ((o := os).remove('x')), either branch of a conditional expression
    ((os if c else x).remove('x'), o = os if c else None), and a tuple or list element indexed by an
    integer literal ((os,)[0].remove('x'), [x, os][-1]), and (round 25) any operand of or and and
    ((os or 0).remove('x'), (1 and os).remove('x'), o = os or None), a shutil or pathlib removal through
    a new name or such an expression being denied already by its attribute (s = shutil; s.rmtree('x'),
    (s := shutil).rmtree('x')), or (round 25) through methodcaller (operator.methodcaller or a
    from-import of it) with a literal removal name, judged as getattr with that name is (a name other
    than remove denies wherever it is; methodcaller('remove', 'x') denies when applied at once to an os
    module, operator.methodcaller('remove', 'x')(os)); or whose text (as written
    or after NFKC folding) names subprocess, system or popen and also holds a removal word or a round
    15 removal form (a shell removal run through subprocess, os.system or os.popen, such as
    os.system('git clean -fdx') or subprocess.run(['cargo', 'clean'])); for ipython, also a program
    that names get_ipython and holds a removal word or form, and IPython shell syntax: a line that
    starts with ! or !! (also NAME = !cmd), the rest of a %sx or %system line, and the %%bash, %%sh or
    %%script cell magic (also %%sx, %%system and %%!) with its program and the lines after it, each
    checked as a shell command string; an ipython program that ast cannot parse and whose text holds a
    removal word or a round 15 removal form denies as cannot-parse;
  * as cannot-parse (rounds 18 and 19), when the command text holds a removal word or a round 15 removal
    form anywhere: a shell, at, batch, python, perl, source or . (also behind the wrappers it knows) that
    reads its program from its standard input, or from a process substitution, /dev/stdin, /dev/fd/N,
    /proc/PID/fd/N or -, in a command that feeds a standard input or file descriptor anywhere (a pipe, also
    one continued onto the next line, an input redirection or duplication, a here-document or
    here-string, a process substitution or coproc); (round 20) so do su with no -c string (su, su -, su
    USER, also sudo su and exec su), sudo -s, sudo -i and doas -s with no command, ssh with no remote
    command, awk -f or sed -f given such a file, and a shell or reader behind a command word it does not
    know (chroot /srv sh); (round 25) so does a shell -c (also fish --command) with no string operand
    behind xargs, which takes its string from the input xargs reads (echo 'rm -rf x' | xargs -0 sh -c,
    also with -d or without either); (round 26) so does, behind xargs, any command whose program comes
    from an operand (a shell, su or flock -c or --command string, a python or ipython -c program, a perl
    -e or -E program, an awk or sed program without -f) when that operand is missing or holds the xargs
    replace string of -I, -i or --replace (printf 'rm x' | xargs -0 -I{} sh -c '{}', xargs -0 su -c,
    xargs -0 python3 -c, xargs -0 awk); over-denies this adds: such a command next to a removal word
    that is only data (find . -name '*.rm' | xargs -I{} sh -c 'echo {}'); (round 27, qanorm26 F1 to F3)
    so does, behind xargs with any options, a program that can run code or commands it is given,
    whatever its operands are: a shell, su, python, ipython, perl, awk, sed, find, fd, ssh, eval, git,
    at, batch, or a wrapper or runner it knows (env, sudo, doas, nice, timeout, flock, setsid, uv, pipx,
    poetry and the rest), an expansion, or a command word it has no rule for with a later unquoted word
    that names one (printf 'rm x' | xargs -0 sh -c '$0', xargs -0 perl -e 'eval shift', xargs -0 -I{}
    ssh host '{}', xargs -0 -I{} git rebase -x '{}' main, xargs -0 -I{} find . -exec sh -c '{}' \\;);
    so does such an xargs that reads, with -a or --arg-file, a file the command writes, with or without
    a fed input (printf 'rm x' > c.txt; xargs -a c.txt -0 sh -c); (round 28, qanorm27 N1) any -a or
    --arg-file file counts as written whenever the command writes any file, as for round 20, not only
    one whose path text matches (cd /tmp; ... xargs -a c.txt, xargs -a ~/c.txt, cp c.txt d.txt; xargs -a
    d.txt); (round 28, qanorm27 N2) so does the same class behind GNU parallel, sem, xe or rush whose
    input is fed, or comes from parallel ::: arguments or (in a command that writes any file) an argument
    file: any word of its command, quoted or not and split at blanks, that names such a program or is an
    expansion, a parallel or sem with no command word (which runs each item as a command), and any rush
    (which runs its command line through a shell with the item in it) (printf 'rm x' | parallel sh -c,
    parallel sh -c ::: 'rm x', parallel ::: 'rm x', printf 'rm x' | rush 'sh -c {}'); over-denies this
    adds: any such xargs, parallel, sem, xe or rush
    next to a removal word that is only data (git ls-files -d | xargs git rm --cached,
    find . -name '*.rm' | xargs sed -n 1p, ls | xargs nice wc -l rm-list.txt), and (round 28) an xargs -a
    of a file the command did not write, or a parallel, sem, xe or rush with no fed input, in a command
    that writes some other file (ls > out.txt; xargs -a list.txt sh -c 'wc -l "$@"' _; echo rm); (round
    29, qanorm28) the guard reads the options of parallel, sem and xe, so an option value given as a
    separate word is not a command word (printf 'rm x' > c.txt; parallel -a c.txt, printf 'rm x' |
    parallel --joblog log), an option it does not know is read as taking the next word as its value,
    and so does, in that class, xe -s, which runs its script through sh with the items as arguments
    (printf 'rm x' | xe -s '$1'; xe -a or -A, items from the command line, counts as an input), a
    replacement string ({}, {1}, {.} and the like, the -I or --replace= value) or a word starting with $
    as a command word of the line (printf 'rm x' | parallel {}, parallel {} ::: 'rm x', parallel -I@ @,
    sem {}), a command substitution in a word ('$(echo {})', '`echo {}`'), and a runner word with its
    quotes and backslashes removed ('"sh" -c', 's\\h -c'); whatever the input, a removal command name as
    a command word of a parallel, sem, xe or rush line or of an xe -s script, quoted or not, or a round
    15 removal form in it (find . -name '*.tmp' | parallel 'rm {}', xe 'rm', parallel 'rm x' ::: a);
    a command word of the line is its first word and the first word after a shell operator, $( or a
    backquote; over-denies this adds: an option that takes no value and that the guard does not list,
    whose next word it reads as a value (with a removal word in the command, parallel --unknown-flag
    echo has no command word); a shell -c string that runs
    such a reader reads it
    from the outer shell's input; a shell -c, python -c or perl -e program that runs its later
    arguments ("$@", $*, $0 to $9, ${!#}, BASH_ARGV, a for or select loop with no in list, sys.argv,
    sys.orig_argv, @ARGV, perl shift or pop), whose later words are read as a command, and (round 20)
    whose later words, quoted or not, hold a removal word or a round 15 removal form anywhere, since it
    may run one as a command string (sh -c '$1' _ 'rm -rf x'); and (round 20) a reader given a script
    operand (a shell, python or perl script, awk -f or sed -f, source or .), or a command word that is
    a path the command writes (./c.sh), in a command that writes a file (an output redirection to a
    file other than /dev/null, /dev/zero, /dev/tty, /dev/stdout and /dev/stderr, which cannot hold a
    script, or tee; round 29, qanorm28: also any other /dev/ path such as /dev/shm/c.sh or /dev/fd/3,
    an operand of cp, mv, install or ln, the of= value of dd, and a python -c or perl -e program whose
    text holds open, write, copy, move, rename, symlink, link or system, or is an expansion), and (round
    29) a shell or su -c string in such a command that names a reader, xargs, . or a path the command
    writes (echo 'rm x' > c.sh; sh -c 'sh c.sh'); the same writes count for the xargs -a rule above;
    over-denies round 29 adds: a reader or such a -c string next to a removal word that is only data in
    a command that writes /dev/shm or /dev/fd/N, copies a file, or runs such a python or perl program
    (cp a b; bash build.sh; git commit -m 'remove x') (see RESIDUAL, Round 18, Round 19 and Round 20).
It allows the same words in a quoted string, a comment, an argument of echo, printf or another bash
builtin that never runs an operand, and a word of any other command that is not exactly a removal command
name (grep -r 'rm' src, grep remove f, tee rm.log); git rm without -f or --force and git rm --cached;
a function definition named after a removal program (rm() { ...; }, as function rm { ...; }), whose body
it still checks; and --rm flags. (Round 37: this inner layer allows them; the broad layer below refuses
rm --help, rm() { ...; }, function rm { ...; }, docker run --rm, tee rm.log and find . -name -delete, and
every other such command whose removal word is outside the exceptions it lists; one exception is the
grep pattern, so grep -r 'rm' src stays allowed.) Round 38 (qanorm37 F3): so the guard as a whole allows, of these, only a removal
word in the text the broad layer exempts (grep -r 'rm' src, grep remove f, git commit -m 'remove x':
see BROAD LAYER); it refuses echo rm, printf '%s' rm, echo 'rm -rf x', ls # rm x, git rm x, git rm
--cached x and git rm -n x, as their text holds rm. It does not allow an unquoted removal command name as a later word of a
command word it has no rule for (docker rm c, grep rm f: see FAIL-SAFE). It does not allow them
anywhere in a command that holds a here-string, nor in a command whose here-document body holds a removal
command in command position (see FAIL-SAFE). Every such allow is then subject to the broad layer below,
which refuses most of them. A command substitution
executes even inside double quotes or an unquoted here-document body, so a removal in one is denied
(a backquote directly inside double quotes whose body holds \\" is cannot-parse instead: see FAIL-SAFE).

BROAD LAYER (round 32, D-2385). Every rule above and in FAIL-SAFE is the inner layer, and it runs first;
a command it denies stays denied, with its own message. A command the inner layer allows then meets
an outer layer that reads text only: it is refused in the safe direction (the broad-refusal verdict) when
its text holds a removal word (the FAIL-SAFE list: rm, rmdir, unlink, shred, srm, wipe, delete, remove,
removedirs, rmtree and getattr, as written, after decoding and quote removal, or after NFKC folding) or a
destructive git form (the round 15 removal forms of _removal_form_in: git clean, git reset --hard, git
stash -u or -a, git checkout or switch -f, git checkout-index -f, git submodule deinit or update -f, git
read-tree -u --reset, git rebase, am, cherry-pick or revert --abort or --skip, git merge --abort,
and also cargo clean and rsync
--delete), read as a word test over the whole text in any order. The outer layer does not read only
these text-only shapes, the whole exception list:
  * git commit message text: the value of -m, --message, -F or --file (also -mTEXT, an -am cluster and
    --message=TEXT), in a simple command at the top level of the command whose command word is git
    (after the git options it knows) and whose subcommand is commit;
  * gh pr and gh issue body text: the value of -b, --body, -F or --body-file (also --body=TEXT), in a
    top-level simple command gh pr ... or gh issue ...;
  * grep and rg patterns: the value of -e or --regexp, or, when there is no -e, --regexp, -f or --file,
    the first operand, in a top-level simple command whose command word is grep or rg; an expansion or
    an option it does not know before the end of the options ends that reading, and then no operand is
    a pattern; the value of a value option it knows is skipped and is not a pattern (rg --pre COMMAND
    is such an option: in rg --pre 'rm -rf x' foo ., foo is the pattern and the --pre value is read);
  * the body of a top-level here-document with a plain delimiter (a name, bare or in single quotes; a
    bare one only when the body holds no $, backquote or backslash) that such a git commit reads with
    -F - (or --file=-), or such a gh pr or issue reads with -F - or --body-file -.
Round 33 (qanorm32 F3, F4): the command word of each of these must be exactly git, gh, grep or rg as
written (not a path such as ./git or /tmp/x/git, not quoted or escaped), with no NAME=VALUE word before
it, and no exception applies when the command text outside the exempt text holds the word PATH as
written (a command that sets PATH, PATH=.:/usr/bin; git ..., may run another program under that name)
or, after quote and backslash removal, defines a function named git, gh, grep or rg (git() { ...; },
function gh { ...; }). Round 33's PATH test read the raw text only, so a quoted or escaped spelling
(export PA"TH"=., declare -x PA''TH=., printf -v PA"TH", read -r PA"TH", declare -n p=PA"TH") passed
it (qanorm33 N1). Round 34 (qanorm33 N1 to N4) adds, and no exception applies when, outside the exempt
text: the word PATH appears after line-continuation, quote and backslash removal (so any binding of PATH
whose name is written in the command: an assignment, export, declare, typeset, local, readonly, printf
-v, read, getopts, mapfile, declare -n, for or select); export, declare, typeset, local, readonly, read,
getopts, mapfile, readarray, unset or printf -v has an operand that holds an expansion (a name built at
run time, n=PA; export "${n}TH"=.); a git command has -c, --config-env or --exec-path before its
subcommand, or is git config, or is a git commit with -e, --edit, -c, --reedit-message (or an
abbreviation of either long option, or a short option cluster holding e or c) or --fixup=amend: or
reword: (each may start the editor, core.editor or GIT_EDITOR, on the message file); gh has -e or
--editor, or is gh config or gh alias; the text, after quote and backslash removal and in any letter
case, holds hookspath, commit_editmsg, git_config, git_exec_path, .git/hooks or .git/config; or any
simple command (also inside a substitution, and behind the wrappers the inner layer knows) has as its
command word a shell, su, python, perl, ssh, at, batch, source, ., eval, xargs, find, fd, sed, awk,
env, parallel, sem, xe or rush, or a command word built at run time, or has such a word later in the
argv of git or of a command word the guard does not know (sh .git/COMMIT_EDITMSG, source ./env.sh,
chroot / sh f, git bisect run sh f), since each may run exempt text that the same command stored.
An exempt word is skipped only when it holds no expansion ($(, ${, $[, $', $", a backquote, <( or >( ),
or when it is exactly the git commit here-document shape "$(cat <<'EOF' ... EOF\\n)" (also <<EOF and
<<-EOF; a bare delimiter only with no $, backquote or backslash in the body) with no earlier delimiter
line in the body and (round 33, qanorm32 F1) no body line that starts with the delimiter after leading
spaces or tabs: bash 5.3.9 ends a here-document inside $( ) at a line EOF)", which this lexer reads as
body, and runs the lines after it (witnessed by qanorm32; that bash ends it at no other line shape is
inference, not witnessed). A body line such as EOF handling: ... therefore loses the exemption.
Over-refusals this adds: every ordinary command whose text holds a removal word or
form elsewhere (echo rm, docker run --rm, kubectl delete pod x, git rm --cached x, git clean -n, git
status; make clean, sed 's/remove/x/' f, ls | xargs grep -l remove, sudo git commit -m 'remove x', a
gh title with a removal word); the self-test pins which of its allow rows the broad layer refuses, by
row id (_BROAD_REFUSED_ALLOW_ROWS; round 32 pinned only their count). Round 34 adds one: source ./env.sh
&& git commit -m 'remove x'. Round 50 (grc review of round 49) names one more: a patch here-document
whose diff holds a line with a removal word, such as -rm x; in a hunk that edits a script (patch -p1
<<'EOF' with --- a/build.sh, +++ b/build.sh, @@ -1 +1 @@, -rm x; and +echo x;), is refused by the broad
layer, as a patch body is not exempt text (probed through decide_raw at round 50: broad-refusal, the
inner layer allowing; a broad row of the self-test pins it). Round 51 (grc review of round 50): the same
removal word on a context line, which a diff writes with a leading space ( rm x; in a hunk @@ -1,2 +1,2 @@
with  rm x;, -echo a; and +echo b;), is refused earlier, as cannot-parse, by the inner layer's
here-document command-position rule (the body line is a removal command in command position after the
space), so this over-refusal reaches every patch here-document that keeps such a line as context (probed
through decide_raw at round 51: cannot-parse, broad-refusal with that rule reverted, allow with the deny
logic off; a cannot-parse row of the self-test pins it).
Round 53 (grc field data from the live guard, not reproduced here): within minutes the broad layer
refused four of grc's own record or memory lines that erased nothing. The guard's own name trips it:
written with a hyphen or a space (no-remove-guard, the no-remove guard), its middle word remove is a
removal word; the file name no_remove_guard.py does not, as the removal-word test reads an underscore
as part of the word. A record, ledger or memory line that only mentions a removal word is refused like
any other text: a ledger line saying the session must never use rm, or a memory index line linking a
note whose name holds a removal word at a hyphen boundary (feedback-delete-policy.md). Reissue the line
without the word, as the broad-refusal message advises (grc reports that this worked each time). Four
broad rows of the self-test pin these shapes with synthetic lines (probed through _evaluate at round 53:
broad-refusal, the inner layer allowing; the same lines with the word taken out were allowed, and no
allow row pins that).
Round 35 (qanorm34 N2: B1, J1, J2, D1). Rounds 32 to 34 withdrew the exceptions for named shapes (a
denylist), and each round left a way to run the exempt text in the same command: git rebase -x, submodule
foreach and bisect run fed "$(git log -1 --format=%B)", a hook written under .git//hooks, rg --pre sh on a
file the command filled, watch or chroot fed the message. Round 35 makes the exceptions an allowlist: they
apply only when the whole command is one simple command of an allowlisted form (_allowlisted_command), and
any other command gets no exception and is judged on its whole text. The allowlist, in full:
  * git [-C DIR] [-P | --no-pager] commit with only these option words: -m, -F, --message, --file,
    --author and --date (each with its value: the next word, after =, or attached to a short letter), -a,
    -q, -s and -n (also as clusters such as -am or -qm'...'), --all, --quiet, --signoff, --allow-empty,
    --allow-empty-message, --amend, --no-edit and --no-verify, then operands (pathspecs) and --;
  * gh pr or gh issue, then create, edit or comment, with only these option words: -t, -b, -F, -B, -H,
    -l, -a, -m, -R, -p and -T with a value, -d, --title, --body, --body-file, --base, --head, --label,
    --assignee, --reviewer, --milestone, --repo, --project, --template, --add-label, --remove-label,
    --add-assignee, --remove-assignee, --add-reviewer, --remove-reviewer, --add-project and
    --remove-project with a value, and --draft, then operands;
  * grep with only the options _GREP_SPEC names (grep runs no program), and --color= or --colour=;
  * rg with only the options _RG_ALLOW names: _RG_SPEC without --pre, --pre-glob, --hostname-bin, -z and
    --search-zip (each runs a program), and without --type-add, --type-clear, --generate, --colors,
    --path-separator, --ignore-file, --engine and the other options it does not list (round 36,
    qanorm35 R2: each short option on the list is there with its long spelling, among them -L and
    --follow, -u and --unrestricted, -b and --byte-offset, -p and --pretty, -h and --help, -V and
    --version, and _RG_SPEC now names --pretty, --help and --version, so the two spellings of an option
    get the same verdict);
and in every form: the command word exactly git, gh, grep or rg as written, no NAME=VALUE word, no $,
backquote, <( or >( anywhere outside the exempt text (so no command or process substitution and no
variable, parameter or arithmetic expansion, even in a single-quoted word, which is refused in the safe
direction), no operator (no pipeline, ;, &&, ||, &, newline list, subshell, group or compound command), no
redirection (not even 2>/dev/null or > file) except the exempt here-document that git commit -F - or gh
--body-file - reads, and no second command. A long option matches only as written, not as an
abbreviation. The round 33 and round 34 withdrawal tests (exact command word, function shadowing, PATH
binding, git editor and configuration, exempt text runner) stay in place behind the allowlist; the self-test
reverts the allowlist together with each of them to show each still refuses its rows. Over-refusal this
adds on the allow corpus, 150 to 155 rows: ls | grep 'rm', cat notes | grep -c remove, echo xargs sh |
grep -c 'rm', echo parallel sh | grep -c 'rm' and cp a.txt b.txt; git commit -m 'remove x'; outside the
corpus, any exempt command with a redirection, behind a list or a pipeline, or with an expansion
elsewhere (git commit -m 'remove x' 2>/dev/null, cd src && rg 'os[.]remove'). Residual: an allowlisted
command still runs programs that configuration or files set outside the command choose, and the guard
reads none of them: a git hook (pre-commit, commit-msg) or core.hooksPath, core.editor or gpg.program
already in a repository, user or system configuration (git commit with -m does not start the editor),
-C DIR naming a repository whose configuration sets such a hook, a gh alias or extension, an rg
configuration file named by RIPGREP_CONFIG_PATH set before the command, and git, gh, grep or rg found on
a PATH set before the command; and a later, separate command (another tool call) may run text an earlier
command stored, which no single-command test can see.

FAIL-SAFE. When it cannot parse a command whose raw text holds a removal word (rm, rmdir, unlink, shred,
srm, wipe, delete, remove, removedirs, rmtree), as written, after $'...' decoding (a $' it cannot
decode is skipped and the text after it still decoded) and the removal of quotes, backslashes and line
continuations, or after that removal with no decoding, each also after NFKC folding (as python folds
identifiers), it denies and says so in the message. The word getattr counts as a removal word for this
test and wherever below the raw text is said to hold a removal word (ast may fold the name getattr takes
from escapes or adjacent literals). Round 22 (qanorm21 N1): a top-level command it cannot parse whose
text holds a round 15 removal form (git clean, git reset --hard, git stash -u, git checkout -f, cargo
clean and the like, read as for a shell -c string) denies the same way. Constructs that bash runs and
that it cannot parse include a named coproc (coproc NAME { ...; }, whose NAME it reads as a command
word), case inside $( ) and an extglob pattern (!(x), @(x) and the like). A command it cannot parse and
that holds none of those words or forms is allowed.
A command that holds a here-string operator (<<<, wherever the lexer reads it as an operator, so not
inside quotes, a comment or arithmetic, but also inside a substitution) counts as a construct it cannot
read exactly: when the raw text (as written or decoded as above) holds a removal word anywhere, the
command is denied as cannot-parse. Round 32 (D-2384) narrowed the here-document rule (<< and <<-): a
here-document denies as cannot-parse only when a body, as the lexer reads it, holds a removal command in
command position (see _body_runs_removal: on a body line, split at ;, &, |, &&, ||, (, ), {, }, $( and
backquotes, a segment whose first word, after NAME=VALUE words and !, if, then, elif, else, do, while,
until and time, is a removal command name, or is a shell, su, interpreter, find, fd, ssh, eval, wrapper
or runner the guard knows, or git, cargo, rsync, gio, xargs, parallel, sem, xe, rush, jobs, source or .,
with a removal word or a round 15 removal form on the line from that segment on), with or without a
removal word elsewhere; so the body of a git commit or gh pr create here-document passes the inner
layer, and a removal word elsewhere in the text meets the broad layer. Round 33 (qanorm32 F2) applies
the same name test to every command word that the inner layer's own split finds in the whole body and in
each body line it can read, which skips redirections (2>/dev/null rm, >f rm, 2>&1 rm, &>/dev/null rm),
coproc, time -p and the reserved words it knows, and a here-document nested in the body; a body line it
cannot read is split as text without splitting a redirection, skipping redirection words, coproc and
time options before the command word (see _body_command_words_run_removal). Round 34 (qanorm33 N3):
round 32 moved python3 -c "$(cat <<'PY' ... os.remove ... PY\n)" from cannot-parse to the broad layer,
as the body test reads shell command position, not the program an interpreter runs; a shell, su,
python or perl argv (behind the wrappers it knows) whose -c or -e program is a word holding an
expansion (that here-document shape, x=$(cat <<'PY' ...); python3 -c "$x", sh -c "$(git log -1
--format=%B)") now denies as cannot-parse when the text holds a removal word (see _expanded_program).
Round 34 (qanorm33 N4): a shell, source or . reading standard input, a process substitution or
/dev/fd/N behind uv run, pipx run, poetry run or jobs -x (read as behind a command word it does not
know), or source or . behind flock, is read as a reader (uv run sh < <(...), poetry run . <(...),
flock /tmp/l . <(...)). Rounds 8 to 10 each found a new
way for here-document tracking to fall out of step with bash, and round 11 found another (a delimiter
line that also carries the ) closing a substitution: for echo $(cat <<EOF followed by the lines hi and
EOF), bash ends both the here-document and the substitution on that last line). Up to round 31 this rule
did not use that tracking; from round 32 it does: a line that the tracking wrongly reads as body is
checked by the command-position test above and by the broad layer (unless it is in an exempt body), and
a removal there that neither reads is not caught (see RESIDUAL). The lexer still reads here-document bodies
as text, and still treats a delimiter line that never comes, a delimiter that holds $( ), ${ }, $[ ] or
a backquote, and a here-document whose substitution or backquote closes before its body is read as
commands it cannot parse; it keeps that reading only so that a command with no removal word stays in
step and is allowed (a body line is data, not a command; the python check can match a removal call,
such as getattr(os, "re" "move"), whose text holds no removal word other than getattr). An env -S
string that forms a removal word once its ${NAME} references are removed, or once its backslash
escapes are removed or read as separators, counts as a command it cannot parse too. An unknown option of a
wrapper it looks past is treated the same way. In find and fd, the value of an option it knows is skipped
as that value (find . -name -exec -delete denies for its -delete; find . -name -delete passes this inner
rule, as find reads that -delete as the pattern, and the broad layer refuses it for its text, round 37;
find . -name x -delete denies); an option word it does not know, which may take a value, before
a later exec option, and an fd option value that is itself an exec option (fd may refuse a value that
starts with - and read it as an option), deny as cannot-parse when a removal word follows. As GNU find
does, a find -exec or -execdir block ends at ; or at a + right after a word holding {}, and an -ok or
-okdir block only at ;; an expansion inside a block (which may become ;, {} or several words), or an
unquoted expansion in a find option value (which may become no word), denies as cannot-parse when a
removal word follows it (or, for a value, when an exec option and a removal word follow it, or a
-delete follows it: find . -printf $E -printf -delete, find . -printf {,} -printf -delete,
find . -newermt $E -printf -delete and find . -fprintf $F $E -printf -delete, where a value that becomes
no word shifts that -delete into primary position). Some constructs parse but cannot be read exactly; when the
raw text (as written or decoded as above) also holds a removal word, the command is denied as
cannot-parse rather than lexed further: a line continuation inside a word (a name or a here-document
delimiter; the test matches any backslash-newline not right after a space or tab) or anywhere in a
command with a here-document; a backquote directly inside double quotes (not one inside a ${...}
there) whose body holds \\" (bash reads that \\" as ", which this lexer does not); a $'...' string
that decodes to a NUL (the
lexer cuts it at the NUL, as bash does, but the check stays); a quote inside (( )), $(( )) or $[ ];
a # inside an array assignment NAME=( ... ); a command word that starts NAME[ (a subscript holding a
space, a quoted ] or an operator); a word alias, hash, mapfile or readarray anywhere in the command
(aliases, hash -p and -C callbacks); and an fd exec option written attached (--exec=CMD, -xCMD).
The same cannot-parse deny applies, without lexing further, when the raw text holds a removal word and any
of: a bash 5.3 brace or pipe command substitution (${ followed by a space, tab or newline, or ${|), whose
body this lexer does not walk; any dollar-quote ($'...' or $"..."; bash keeps only the low 8 bits of an
octal escape, which the decoder here does not); env given -S or --split-string anywhere among its words
(a repeated -S is not modelled); the name BASH_CMDS or BASH_ALIASES anywhere (an assignment to either
edits the command hash or the alias table, as hash -p and alias do); or one of the string-evaluation
builtins named in the bash manual as a word of the command: eval, trap, let, bind, complete, compgen, fc
or enable (each runs or evaluates a string, or changes what a command name runs; with alias, hash, mapfile
and readarray above).
The time reserved word followed by a word that starts with - other than -p also counts as a command it
cannot parse. A command word built at run time (an expansion, substitution or glob) denies as
cannot-parse when its own text or a word of its argv holds a removal word. After a redirection, as in
bash, it reads no later word of that simple command as a reserved word ([[, case, !, { and the like).
Round 16: a command word it has no rule for (anything but the commands, wrappers and runners named in
WHAT IT DENIES and the bash builtins that never run an operand: echo, printf, :, true, false, test, cd,
pwd, pushd, popd, dirs, export, declare, typeset, local, readonly, unset, shift, return, exit, read, set,
shopt, umask, ulimit, wait, type, help, getopts, times, logout, disown, suspend, kill, caller and
history; round 17: not jobs, whose -x runs a command) counts as a command it cannot parse when a later
unquoted word of its argv is a removal command name (rm, rmdir, unlink, shred, srm, wipe, or a path ending in one), or is git followed by a form the git
rules deny or count as cannot-parse, because the command word may be a wrapper it does not know. Measured
on the round 16 corpus, this denies these commands, which remove nothing: grep rm file, grep -r unlink
src, grep -c shred notes.txt, rg rmdir ., ls | grep rm, xargs grep rm < list, find . -exec grep -l rm
{} +, docker rm container, docker rm -f c, podman rm c, npm rm lodash, pnpm rm lodash, npm run rm, brew
rm wget, which rm, man rm, whereis rm, info rm, ls rm, cat rm, cp rm /tmp/x, diff rm a, chmod +x rm, tar
-czf a.tgz rm, make rm, ln -s /bin/rm /tmp/zz, grep git clean, and foo git rm x; quote the word ('rm')
to pass such a command. It also denies, as cannot-parse, forms that do remove: toybox rm -rf x, chroot
/srv rm -rf x, watch -n 1 rm x, parallel rm ::: a b. Round 23 (qanorm22 F1): an unquoted cargo or rsync
word followed by a form the cargo or rsync rule denies counts the same way (chroot /srv cargo clean,
mywrap rsync -a --delete a b), so grep cargo clean and grep rsync --delete f are denied too; an
unknown command word before an ordinary cargo or rsync call (time-it cargo build) is allowed. It
allows type rm, help rm,
command -v rm, sed -n /rm/p f, grep 'rm' f, tee rm.log and git grep rm (git is a command it has rules
for).
Every internal error, an unreadable payload (not JSON, not
an object, no tool_name, no tool_input object, a command that is not a string or holds a NUL) and a
missed internal deadline deny. Round 52 (grc review of round 50): an unreadable payload denies with a
reason of its own, which says the hook input was malformed and gives no file-removal advice; an
internal error, a missed deadline and a stdin read failure keep the internal-error reason.
A deny is written in the repository hooks' output contract (exit 0, hookSpecificOutput with
permissionDecision "deny" and a permissionDecisionReason, plus a systemMessage); an allow is no output
and exit 0; if the deny itself cannot be written it exits 2 with a note on stderr.

RESIDUAL. This guard is defence in depth, not a boundary. It does not catch:
  * variables and expansion (a command word or option built at run time, such as "$X", r$EMPTYm, a glob
    or a brace expansion, which it counts as an unquoted { with a , or .. before its closing }; a command
    word built at run time is denied only when a removal word is in its own text or its argv, as
    FAIL-SAFE says, so r{m,} x, which bash runs as rm r x, passes);
  * aliases, hash -p entries and functions defined outside the command it is shown, and (round 47,
    qanorm46 M3, B2) an alias or an exported function defined inside it, as the next item says;
  * (round 47, qanorm46) these forms, each allowed at this head (an allow row of the self-test pins each
    verdict), which make bash or the program run a command the guard never reads, here git restore
    --ours (which overwrites a conflict resolution made by hand) or any other command; what xe, GNU
    parallel, sem and rush do with them is inferred from their documentation, not witnessed (none was
    installed where the review ran):
    - (B1) xe -p, pattern mode: the PATH_APPENDERS entry for xe reads -p as a plain flag, so the guard
      checks only the first word after the options (a pattern) as the command word, never reads the
      command after each +, and does not split the shell line there: ls | xe -p cat cat + '*'
      env -S'git restore --ours' runs env -S'git restore --ours' on each item that does not match cat
      (the same env -S form at top level is denied);
    - (B2) an exported bash function that takes over a program name: a BASH_FUNC_NAME%% setting given by
      env or export in the same command, which a bash started later imports as the function NAME
      (witnessed for bash -c on the review host; that GNU parallel and sem run their command through bash
      when started from bash is inferred), so a listed plain program behind a path-adding program runs
      the function instead: ls | env 'BASH_FUNC_grep%%=() { git restore --ours "$@"; }' parallel grep x
      and export 'BASH_FUNC_grep%%=() { git restore --ours "$@"; }'; ls | parallel grep x; and at top
      level, env 'BASH_FUNC_x%%=() { git restore --ours f; }' bash -c x. The function written out
      (grep() { git restore --ours "$@"; }; export -f grep; ls | parallel grep x) is read and denied;
    - (M1) a setting whose name is built at run time: _APPENDED_SETTING matches only a name written out,
      so a name built from a variable passes (v=PARALL; export "${v}EL=-I log"; echo restore | parallel
      git log --ours f, and v=GI; export "${v}T_EXTERNAL_DIFF=./fix.sh"; ls | xargs git diff; the review
      found the same for PATH and GIT_CONFIG_PARAMETERS, and the same match misses any such name built
      that way), and so do names given by export $(...)
      (export $(cat env.txt); ls | xargs git diff), while the written-out export PARALLEL='-I log' form is
      cannot-parse (that bash's export takes an expanded name is inferred, not witnessed);
    - (M2) GNU parallel and sem --parens, in any letter case or abbreviation (--PARE), which changes the
      delimiters of the perl expression: the guard looks only for a literal {=, so an expression in other
      delimiters is not read (ls | parallel --parens ,,,, grep x ',,system "gi"."t restore --ours f",,',
      and the --PARE and sem forms); an expression that writes git or unlink out is still cannot-parse
      or refused by the broad layer;
    - (M3) an alias defined earlier in the same multi-line command (witnessed for bash -c on the review
      host): the three lines shopt -s expand_aliases, alias xargs='env -S"git restore --ours"' and ls |
      xargs grep x, and the three lines shopt -s expand_aliases, alias ll='git restore --ours' and ll f
      (the word alias makes a command cannot-parse only when its text also holds a removal word);
    - (m1) GNU parallel --limit, which runs the command it names and is not in _APPENDED_PROGRAM_LONG
      (ls | parallel '--limit=./x.sh' cat), and the options that write, replace or empty a file it names:
      GNU parallel --joblog, --results and --tmpl (ls | parallel --joblog src.c cat, ls | parallel
      --results src.c cat, ls | parallel --tmpl a.tmpl=src.c cat) and rush -o (ls | rush -o src.c cat);
  * (round 48, grc review of round 47) these forms, each allowed at this head by both layers (each was
    probed through decide_raw, and an allow row of the self-test pins each verdict; round 49, grc review
    of round 48: patch --remove-empty-files, the long spelling of patch -E, is not among them, as the
    MED-2 entry says, while round 50, grc review of round 49: its abbreviations --rem, --remo and --remov
    are among them); what each removes is taken from the documentation of git, GNU patch, pip, npm and
    cargo, recalled and not witnessed (none was run):
    - (MED-2) a diff that deletes a file, applied by git apply, git am or patch. A diff whose header holds
      deleted file mode, or whose new-file line is +++ /dev/null, removes that file from the working
      tree; git apply -R and patch -R remove a file that the diff creates; patch -E removes a file the
      patch leaves empty; git am also commits the removal. The
      diff may be a file (git apply fix.patch, git apply -R fix.patch, git am 0001-drop-old.patch, patch
      -p1 < fix.patch, patch -R -p1 < fix.patch, patch -E -p1 < fix.patch) or a here-document in the same
      command (git apply <<'EOF' with the lines diff --git a/old.c b/old.c, deleted file mode 100644, ---
      a/old.c, +++ /dev/null and a hunk; the same diff after a mail header given to git am; a --- a/old.c,
      +++ /dev/null hunk given to patch -p1 or patch -E -p1): the guard reads neither a diff file nor a
      here-document body as a diff, and none of the words of these forms is a removal word. Round 49
      (grc review of round 48): the long spelling of patch -E, --remove-empty-files, holds the removal
      word remove, so the broad layer refuses it (probed through decide_raw at round 49: patch
      --remove-empty-files -p1 < fix.patch and the patch -E -p1 here-document above with
      --remove-empty-files in place of -E each got broad-refusal, the inner layer allowing; a broad row of
      the self-test pins each). Round 50 (grc review of round 49): GNU patch also takes an unambiguous
      prefix of a long option as that option (by its documentation, recalled and not witnessed: --re is
      ambiguous), so --rem, --remo and --remov each mean --remove-empty-files; none holds the word remove,
      and none is a removal word, so both layers allow them, a disclosed residual (probed through
      decide_raw at round 50: patch --rem -p1 < fix.patch, patch --remo -p1 < fix.patch, patch --remov -p1
      < fix.patch and the patch -E -p1 here-document above with --rem in place of -E each got allow, the
      inner layer allowing too; an allow row of the self-test pins the --rem file form and the --rem
      here-document, and round 51, grc review of round 50, adds allow rows for the --remo and --remov
      file forms, probed through decide_raw at round 51: allow, the inner layer allowing too). It loses
      the file at each such path; its content survives only where something else holds it: for git apply
      and patch, HEAD, for a tracked file with no uncommitted change; for git am, which commits the
      removal, not HEAD but the parent of the commit that removes the file (HEAD^ right after git am
      applies a single patch; round 49, grc review of round 48); and the diff itself where it lists every
      removed line;
    - (MED-3) git sparse-checkout set (git sparse-checkout set src): it removes from the working tree the
      tracked files its patterns leave out. Round 49 (grc review of round 48), from git's documentation,
      recalled and not run: in cone mode, the default, it takes directories and keeps every file under
      each named directory, every file directly in the top-level directory and every file directly in
      each leading directory of a named one, so git sparse-checkout set src keeps every top-level file and
      every file under src, and removes the tracked files in every other directory (round 50, grc review
      of round 49: for a deeper set, such as git sparse-checkout set a/b/src, the files directly in each
      leading directory, a and a/b, stay too); in non-cone mode (--no-cone) it takes
      gitignore-style patterns and removes every tracked file they do not match. It loses only their
      working-tree copies: HEAD still holds their committed content, and git sparse-checkout disable
      brings them back (what it does with a file left out that holds uncommitted changes was not
      checked);
    - (LOW-1) git stash drop (one entry, stash@{0} when none is named) and git stash clear (every entry),
      which lose the stashed changes, the local and staged edits a git stash saved, from the stash list
      (until git gc prunes them, git fsck --unreachable may still find the dropped stash commits); and git
      gc --prune=now, which deletes at once every unreachable object of any age, so it loses whatever no
      ref or reflog entry reaches, such as dropped stashes and commits that nothing else holds. None of
      the three removes a working-tree file;
    - (LOW-2) package uninstallers: pip uninstall (pip uninstall -y requests), npm uninstall (npm
      uninstall left-pad) and cargo uninstall (cargo uninstall ripgrep). Each deletes the installed files
      of a package (pip every file the package's install record lists, such as the RECORD file of its
      .dist-info directory, which covers the console scripts it placed in the environment's bin directory
      as well as its files in site-packages (round 49, grc review of round 48); npm from node_modules,
      also dropping the dependency from package.json and the lock file; cargo the binaries cargo install
      placed in its bin directory). It
      loses those files, and any local edit made to them; the package itself can be installed again from
      its index. Up to round 47 only the catch-all for other deletion programs it does not name (below)
      covered them;
  * a removal word that never appears literally in the raw text, even after the decoding above (one built
    from variables, other encodings such as printf or base64 output, or another interpreter), in a
    command whose constructs it cannot read exactly: the cannot-parse check needs the word in the text;
    also a round 15 removal form (git clean, git reset --hard, cargo clean and the like) with no removal
    word, on a line that here-document tracking hides, or after
    an option a wrapper does not know (sudo --unknown-flag git clean -f; round 21 reads an unambiguous
    abbreviation of a long option it knows as that option): outside a shell -c string, a top-level
    command it cannot parse (round 22), a python or perl shell call and a git command string, those
    tests read removal words only;
  * other interpreters (node, ruby, and perl beyond a literal -e or -E program with unlink or rmtree or
    a shell call with a removal word or form: a perl script file, a program on stdin, rmdir, File::Path
    remove_tree, a pipe open such as open(F, "rm x |")), a shell -c string with no removal word or form in
    its own text (one held in a variable, as in bash -c "$CMD"), a shell -c string that sh, dash, zsh,
    ksh, mksh, ash, fish, tcsh or csh reads differently from bash, and eval of a string that holds no
    removal word;
  * other shells: it parses bash only, so zsh, dash, sh or fish forms that bash reads differently pass,
    for example zsh =rm x, which zsh expands to the path of rm; and a -c string of a shell it does not
    name (yash, posh and the like) or of a su-like program other than su (runuser -c; (round 31,
    qanorm30 MINOR-2) sg GROUP -c 'rm x' and sg GROUP 'rm x', since sg runs its command through
    /bin/sh -c by its documentation, inferred and not witnessed), which the round 16 fail-safe for
    unknown command words does not read when the string is quoted;
  * deliberate obfuscation, including these forms that bash runs and this guard allows:
    - a single quote inside ${...} in double quotes, which bash uses only to find the closing }, so a
      $( ) between the quotes still runs (echo "${x:-'$(rm -rf x)'}"), though the broad layer refuses
      it (round 32); the same body line in an unquoted here-document is refused by the broad layer when
      the text holds a removal word outside an exempt body;
    - prompt expansion of a string: PS4='$(rm -rf x >&2)'; set -x; true, and x='$(rm -rf x)';
      echo "${x@P}";
    - arithmetic evaluation of a variable whose value holds an array subscript with a $( ):
      x='a[$(rm -rf x >&2)]'; echo $((x)), and the same x with [[ $x -eq 0 ]]; also a quoted subscript
      given to a builtin that takes a variable name (declare, typeset, local, export, readonly, unset,
      printf -v, read, getopts, test -v, wait -p), which it does not count as string evaluation;
      and the same subscript written literally where bash evaluates it as arithmetic:
      [[ 'a[$(rm -rf x >&2)]' -eq 0 ]], declare -i n='a[$(rm -rf x >&2)]', a['$(rm -rf x >&2)']=1;
    - indirect expansion of a variable whose value holds an array subscript with a $( ):
      x='a[$(rm -rf x >&2)]'; echo ${!x};
    - an octal escape above \\377 in $'...' that bash wraps to a letter (bash keeps the low 8 bits), so
      that no removal word appears in the decoded text, for example $'\\562m' x, which bash runs as rm x;
    - a renamed copy or link of a remover made by an earlier command (ln -s /bin/rm /tmp/zz, then
      /tmp/zz -rf x; in one command, ln -s /bin/rm is denied as cannot-parse by the round 16 fail-safe),
      and multi-call programs given the name in a form that fail-safe does not read
      (coreutils --coreutils-prog=rm, toybox 'rm');
  * a script or build file that is run (./clean.sh, bash script.sh, make clean) and whose contents are
    not in the command text; a script written and run in the same command has its contents in the
    text, and round 20 denies that form as cannot-parse when the text holds a removal word or form
    (see Round 20), but a script written by an earlier command, or one run by a command word that is
    neither a reader nor the path the command writes (chmod +x c.sh; PATH=.:$PATH c.sh), is not seen;
    (round 29) nor is a file written by a program the guard does not list as a writer (rsync, tar,
    curl -o, sed -i, an awk or node program, a python or perl program written without those words, a
    script file), and the written-file context reaches a shell or su -c string one level deep only by
    the names in it (a python or perl program that runs a reader of the written file, or a -c string
    inside a -c string that names only a wrapper the guard does not know, is not read that way);
  * python a literal -c parse cannot see (a script file, python -m, a program on stdin or held in a
    variable, a program produced by a command substitution, such as python3 -c "$(cat prog.py)" or one
    built by echo or printf, whose placeholder text this check parses instead of the program; one fed
    by a here-document with a removal word in the text is refused by the broad layer instead (round 32;
    up to round 31 the here-document rule denied it as cannot-parse); or
    a removal reached through exec, eval, os.spawn*, os.exec*, os.posix_spawn or os.posix_spawnp,
    pty.spawn, asyncio.create_subprocess_exec or asyncio.create_subprocess_shell, a module dictionary
    lookup (os.__dict__["remove"], vars(os)["remove"]), getattr with a name built at run time
    (getattr(os, 're' + 'move'), which does not hold the word remove), an os module bound to a name in a
    way round 23 does not follow (an attribute or subscript target such as d['o'] = os, a for or with
    target, a function argument or default, an import inside exec), an os module reached through a
    globals() or vars() subscript (globals()['os'].remove('x'), vars()['os'].remove('x')) or through
    starred unpacking (*o, = [os]; o[0].remove('x'), or a, *o = 1, os), a tuple or list element
    indexed by anything other than an integer literal ((os,)[i]) or a subscript of a name bound to a
    tuple or list (t = (os,); t[0].remove('x')) (round 24 follows only a walrus, a conditional
    expression and a literal-indexed tuple or list display, and round 25 adds or and and), and (round
    25, qanorm24 MINOR 1) an os module reached through a dict display subscript ({0: os}[0].remove('x')),
    a call (next(iter([os])).remove('x'), o = (lambda: os)()), a comprehension subscript
    (o = [os for _ in '1'][0]) or a starred element of a display ([*[os]][0].remove('x'); an os
    module that is itself an element next to a starred one counts at every index), a methodcaller with
    the name remove that is bound to a name or passed on before it is applied (m =
    operator.methodcaller('remove', 'x'); m(os)) or that is reached under another name (from operator
    import methodcaller as mc), (round 30, qanorm29 F2) operator.attrgetter with a removal name
    (operator.attrgetter('remove')(os)('x')), which no rule reads, and __getattribute__ with one
    (os.__getattribute__('remove')('x'), object.__getattribute__(os, 'remove')('x'),
    type(os).__getattribute__(os, 'remove')('x')), which no rule reads as getattr is read, another name
    it does not track, or a
    subprocess, os.system or os.popen call whose removal word or round 15 removal form is not in the
    program text, for example one built by string joining such as 'git ' + 'cl' + 'ean'),
    and truncation or overwrite from inside a python -c program (open(f, "w"), write_text, os.truncate,
    os.replace or shutil.move over a file);
  * xargs reading names from stdin (for example a command word that xargs -I takes from its input,
    printf 'rm x' | xargs -I{} {}); round 25 denies a shell -c with no string operand behind xargs,
    round 26 (qanorm25 F1) any shell, su or flock -c, python or ipython -c, perl -e or -E, awk or sed
    program operand behind xargs that is missing or holds the replace string, and round 27 (qanorm26 F1
    to F3) any program behind xargs that can run code or commands it is given, only when the command
    feeds an input (or, round 27, its xargs reads with -a or --arg-file a file the command writes; round
    28, in a command that writes any file) and
    its text holds a removal word or a round 15 removal form, so not one whose xargs reads a file in a
    command that neither feeds an input nor writes a file (xargs -a cmds.txt sh -c), and not a program
    that runs its input another way and is not named in WHAT IT DENIES (node, ruby, make, rsync -e);
    round 28 (qanorm27 N2) applies the same class to GNU parallel, sem, xe and rush, under the same
    conditions, and round 29 (qanorm28) reads their options from a short list of flags (which flags
    take no value, that xe -s runs its script through sh with the items as $1 and on, and that xe -a
    and -A take items from the command line are inference from GNU parallel's and xe's documentation,
    not witnessed); other programs of this kind (dsh, pdsh, clush, pssh and the like) are not named;
    a replacement string as the command word behind xargs (printf 'rm x' | xargs -I{} {}) stays
    allowed, as above, while round 29 denies it behind parallel, sem and xe; whether GNU parallel
    quotes a replacement string that forms the whole command, which would make parallel {} harmless,
    was not checked (round 29 denies it in the safe direction, so this is an inference only about
    over-denial); a parallel -a or :::: file in a command that neither feeds an input nor writes a
    file (parallel -a cmds.txt sh -c; echo rm) is not read, as for xargs -a;
  * (qanorm25 F2) a su -c string that runs its later arguments: su -c '$1' root _ 'rm x', su -c '"$@"'
    root _ rm x and sudo su -c '$1' root _ 'rm x' are allowed; the later-arguments rule covers a shell
    -c, python -c and perl -e, not su -c (that util-linux su passes the words after the user name to the
    shell is inference from its documentation, not witnessed);
  * (round 30, qanorm29 F3) a quoted command after sudo -s or -i: sudo -s 'rm -rf x', sudo -i 'rm -rf x'
    and sudo -s -- 'rm x' are allowed, while the unquoted forms (sudo -s rm x, sudo -s 'rm' x) are
    denied. That is harmless only where sudo backslash-escapes the non-alphanumeric characters of a -s
    or -i command, so that the shell receives the one word rm -rf x and finds no such command (inference
    from sudo's documentation, not witnessed); a sudo that does not escape them (another version, or a
    sudo-like program such as sudo-rs) runs the removal, and this guard does not check which sudo runs;
  * (qanorm25 F3) a cron job that removes later: echo '* * * * * rm -rf x' | crontab -, the same with git
    clean, and a crontab file written and installed in one command (echo ... > ct; crontab ct) are
    allowed; crontab is not a reader, so the job runs later outside any command this guard sees (at and
    batch fed that way are denied);
  * truncation, overwrite and move-away forms (: > f, truncate, cp /dev/null, mv or ln over a file, dd,
    tar --remove-files, sed -i, gio trash, trash-put), and (round 48) a diff that deletes a file, applied
    by git apply, git am or patch (also -R and -E, and a diff in a here-document), as the round 48 item
    above says (round 49: the broad layer refuses --remove-empty-files; round 50: -E and the
    abbreviations --rem, --remo and --remov of --remove-empty-files are allowed);
  * at the inner layer only (round 38, qanorm37 F3: the broad layer refuses every git rm, git rm --cached
    included, as its text holds rm, so the guard as a whole refuses it), git rm without -f or --force,
    which deletes the named tracked files from the working tree: git
    refuses to remove a file whose content differs from HEAD (local or staged changes, or a file added
    since HEAD), so what it removes is held in HEAD and git restore --source=HEAD --staged --worktree
    brings it back (rm, by contrast, also removes untracked and modified files). Also a git
    alias that runs rm -f (git config alias.x 'rm -f', which the broad layer refuses for its rm), and git worktree
    remove without -f or --force; git commands that discard working-tree content and that it does not
    deny: git checkout -- . and other git checkout of a path without -f (round 39: and without the
    stage-rewrite options of GIT_STAGE_REWRITE_OPTIONS), git checkout -f WORD with one
    operand that can be a branch name and no -- (qanorm26 F4: by git's documentation, git checkout -f
    main, -f HEAD and -f @ throw away local changes to tracked files as git switch -f does, which this
    guard denies; WORD may be a branch or a path such as src or README.md, and the inner layer leaves
    this form allowed as a known gap, not because the command is safe; the broad layer refuses it, as
    git checkout -f is a round 15 removal form), git restore without a stage-rewrite option (it has
    no force option, and its working-tree form is a routine call), git reset --keep or --merge; (round 37,
    grc round 36 LOW) git restore --source=TREE (or -s TREE) with --worktree, -W or neither --worktree nor
    --staged (its default target), and git checkout --no-overlay TREE -- PATH: in no-overlay mode, git
    restore's default, each removes from the working tree the tracked files under PATH that TREE does not
    hold, and overwrites the rest (by git's documentation, inferred and not witnessed). They are not
    denied because the files they remove are tracked, so the index or a commit still holds their staged
    content, and what can be lost is unstaged local change, which git checkout -- PATH and git restore
    PATH, left allowed as routine calls, also overwrite on a path that is not conflicted. On a conflicted
    path that is not the same loss (round 39, qanorm38 F1, witnessed with git 2.53.0): git checkout --
    PATH and git restore PATH refuse to run there, while git checkout HEAD -- f, git checkout HEAD f and
    git restore --source=HEAD f overwrite an unstaged hand resolution of f (the two checkout forms also
    replaced its three unmerged index entries with HEAD's version); these TREE forms stay allowed as a
    known gap, not because they are safe. Round 40 (qanorm39 F3) states the whole set and the weighing:
    git checkout TREE -- PATH, git checkout TREE PATH, git restore --source=TREE PATH and -s TREE PATH
    (with -W, -S, both or neither), and git restore -SW PATH or --staged --worktree PATH with no source
    (--staged makes HEAD the source), for TREE HEAD (whose version is stage 2, so each writes what --ours
    writes, by git's documentation, inferred and not witnessed), @, a branch, a tag, a commit id or an
    expansion. Round 40 denies them only from MERGE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD, REBASE_HEAD and
    AUTO_MERGE (_GIT_OPERATION_REF; MERGE_HEAD and CHERRY_PICK_HEAD write what --theirs writes, and,
    round 41 (qanorm40 N2), REVERT_HEAD writes the base version, stage 1, as a revert of C merges with C
    as the base; inferred from git's revert design, not witnessed), and round 41 (qanorm40 N4) also from
    FETCH_HEAD, from the main-worktree/ and worktrees/NAME/ spellings of each and in any letter case.
    These refs exist mostly while an operation stops on a conflict, though not only then (round 41,
    qanorm40 N3: MERGE_HEAD also after git merge --no-commit, REBASE_HEAD also at a rebase edit step, and
    FETCH_HEAD after a git fetch that writes it, which (round 42, qanorm41 F4) git fetch --dry-run and
    --no-write-fetch-head do not; by git's documentation, inferred and not witnessed), so a deny
    refuses few routine commands; it over-denies git checkout FETCH_HEAD -- f after a plain fetch, and
    git checkout a MERGE_HEAD, where MERGE_HEAD is a path; (round 42, qanorm41 F2) the match is the whole
    word, in any letter case, or the name followed by a revision suffix (~, ^, @ or :), so a file named
    merge_head or Auto_Merge is still read as the ref (git checkout main merge_head, an over-deny), while
    auto_merge.py, Merge_Head.md and the branch auto_merge-fix are not. ORIG_HEAD stays allowed: during a
    merge it names HEAD's commit, stage 2 (inferred), as HEAD does, and git checkout ORIG_HEAD -- f is a
    routine recovery after git reset; (round 42, qanorm41 F4) during a rebase, though, ORIG_HEAD names the
    branch tip from before the rebase, so at a rebase stop on a conflict git checkout ORIG_HEAD -- f and
    git restore -s ORIG_HEAD f overwrite a hand resolution too (inferred from git's documentation, not
    witnessed); it stays allowed for the recovery use, a known gap. The rest stay allowed because, on a path that is not conflicted, each is the
    routine discard of local change to a tracked file (git checkout HEAD -- f, git restore -SW f, git
    restore -s main f), the guard cannot see the index to tell a conflicted path from another, and a
    deny of every tree source would refuse those routine calls; what each can lose is unstaged change,
    as for git checkout -- PATH. git restore has no tree-ish operand, so for it the reason is that
    routine use alone, not telling a tree-ish from a path; for git checkout TREE PATH it is also that
    TREE may be a path (git checkout a b names two paths when a is no ref). The weighing (qanorm39 F3):
    the round 39 deny of --ours and --theirs is sidestepped by these equally natural commands, and
    (round 41, qanorm40 N6) the round 40 deny of the operation refs is sidestepped just as easily by
    naming the merged branch or its commit id (after git merge feature, git checkout feature -- f writes
    stage 3's version; inferred), and (round 42, qanorm41 F4) after a git stash pop or git stash apply
    that stops on a conflict, by naming the stash (git checkout stash@{0} -- f writes the stashed side;
    inferred, not witnessed), as no stash ref is an operation ref here, so each stops an accidental stage rewrite, not one written to get
    around it; at the inner layer only (round
    39, qanorm38 F4: the broad layer refuses the
    text of each round 15 removal form, these included, and of every command whose text holds a removal
    word, so the guard as a whole refuses git --html-path clean -f, git $OPTS clean -f, git --html-path
    revert --abort and git $OPTS revert --abort), git clean, git reset --hard,
    git stash -u, git checkout -f, git switch -f, (round 31) git rebase --abort or --skip, git am
    --abort, (round 37) git merge --abort, git cherry-pick --abort, (round 38) git am --skip, git
    cherry-pick --skip and git revert --abort or --skip, and the git subcommands that run a command
    whose command holds a removal word or a round 15 removal form, each after a git option it does not
    know or an expansion before the subcommand (git --html-path clean -f, git $OPTS clean -f); (round
    40, qanorm39 F5) not git worktree remove -f there (git --html-path worktree remove -f x, git $OPTS
    worktree remove -f x): its text holds the removal word remove, so the inner layer denies it as
    cannot-parse, as it does without -f; at both
    layers, (round 39) git checkout or git restore with a stage-rewrite option, or (round 41, qanorm40
    N5) with an operation-ref tree, after a git option it does not know or an expansion before the
    subcommand (git --html-path restore --ours f, git $OPTS checkout -m -- f, git --html-path restore -s
    MERGE_HEAD f, git $OPTS checkout MERGE_HEAD f: the broad layer's text test does not hold these forms,
    since -m, --ours and the like are common words in other git commands), and for the same reason one
    inside a python -c or
    perl -e shell call or a script fed to a shell on standard input, which this guard reads by that
    text test only (python3 -c 'import os; os.system("git restore --ours f")', perl -e 'system("git
    checkout --theirs -- f")', echo 'git restore --ours f' | sh); and any of these with an expansion
    that may become
    --hard, -u, -a, -f, --abort, --skip, -m, --merge, --conflict, --ours, --theirs, -2, -3 or a command
    option (round 38, qanorm37 F4: this holds for each
    of those subcommands whose rule above does not deny such an expansion, and the examples that follow
    are not the whole list: git reset $MODE, git stash $OPT, git checkout $OPT -- x, git switch $OPT
    main, git rebase $OPTS main, git am $OPT, git merge $OPT, git cherry-pick $OPT, git revert $OPT,
    and (round 39) git restore $OPT x);
    (round 40, qanorm39 F2; round 41, qanorm40 N1) git checkout or git restore with a stage-rewrite
    option or an operation-ref tree and no path named, behind a program that puts the items it reads or
    the paths it finds into its command, where round 46's allowlist of the command word
    (_appended_command_check) and round 45's allowlist in _appended_git_check (applied to xargs, gxargs,
    fd and fdfind -x, -X, --exec and --exec-batch, find, gfind and bfs -exec, -execdir, -ok and -okdir
    blocks that hold {}, and GNU parallel, sem, xe and rush) do not see the git command: a program of
    that kind the guard does not read (ls | pdsh -w h git restore --ours; dsh, clush, pssh and the like);
    GNU parallel, sem, xe or rush behind a command word the guard does not know (ls | chroot / parallel
    git restore --ours), since the unknown-command scan starts a check from xargs, gxargs, find, gfind,
    bfs, fd and fdfind but not from these four; (round 46) a setting set outside the command text, which
    the command text does not show: GNU parallel options from a PARALLEL variable exported earlier,
    ~/.parallel/config or a profile file (a --rpl or --parens there can make a listed name or subcommand
    a replacement string), and a PATH, LD_PRELOAD, GIT_ variable or other _APPENDED_SETTING name set
    before the command, which can make a listed name run another program (a PARALLEL, GIT_, PATH or other
    such name written out anywhere in the same command text is cannot-parse when such a program is
    checked; round 47: one built at run time, and a BASH_FUNC_ setting, pass, as the round 47 item says);
    an error in the option tables the round 46 check reads to find the command word (WRAPPERS["xargs"]
    and PATH_APPENDERS, recalled from each tool's documentation and not witnessed): a value option listed
    as a flag would make its value the command word, so a listed name written as that value would pass
    while the command after it runs (an option the tables do not list is cannot-parse); what GNU
    parallel, sem and rush do with their command beyond the parts the guard reads: a redirection in the
    shell line they build (ls | parallel grep x {} '>' out.txt), a command run on another host
    (-S host), and (round 47) the --limit command, the files --joblog, --results, --tmpl and rush -o
    write, the command after a + of xe -p and a perl expression in --parens delimiters, as the round 47
    item says; and a find, gfind or bfs block with no {}, to which find appends nothing (find . -name x
    -exec git checkout -m ';'). The allowlists do not stop what a listed program itself does: cp, mv,
    ln, touch, chmod and mkdir change files as they do anywhere, judged by the guard's other rules; and
    (round 46, qanorm45 F3) git log, show, diff, rev-list, shortlog and blame with --output FILE open FILE
    for writing and can empty or replace it, a tracked file, .git/index or a ref file included, as a
    shell redirect does, which this guard does not read either (ls | xargs git diff --output=f, ls |
    xargs git rev-list --output=src.c HEAD, ls | xargs git log --output=.git/HEAD, and, from the items,
    printf -- '--output=.git/HEAD\\n' | xargs git log; echo x > .git/HEAD and git log > .git/index are
    allowed too); and (qanorm45 F5) a listed subcommand still runs the programs that git's configuration
    or the environment names (core.pager, a diff driver, textconv or diff.external program,
    core.fsmonitor; GIT_CONFIG_PARAMETERS, GIT_CONFIG_COUNT with GIT_CONFIG_KEY_n and
    GIT_CONFIG_VALUE_n, GIT_EXTERNAL_DIFF, GIT_PAGER, PAGER, GIT_EDITOR, EDITOR, GIT_SSH_COMMAND), as any
    git command does: at top level (GIT_EXTERNAL_DIFF=./fix.sh git diff, GIT_PAGER=./fix.sh git log) and
    set before the command these are allowed; behind a path-adding program in the same command they are
    cannot-parse (ls | xargs env GIT_EXTERNAL_DIFF=./fix.sh git diff). Over-denies, as cannot-parse,
    behind those programs (round 45 replaces the lists of rounds 43 and 44, which this one holds): every
    git command but the allowed forms. Because
    this guard prefers refusing, that includes common commands that remove nothing: any git option before
    the subcommand (ls | xargs git -C repo log, ls | xargs git --no-pager log, ls | xargs git -c
    'user.name=A B' log, ls | xargs git --version); any subcommand outside the list, read-only ones too
    (git diff --name-only | xargs git add, git log --format=%H | xargs git cherry-pick, ls | xargs git
    grep -l x, ls | xargs git stash show, ls | xargs git worktree list, fd -e c -X git commit -m x, find
    . -name '*.c' -exec git add {} +, ls | parallel git add, ls | xargs git reset, ls | xargs git
    restore, fd -e c -X git restore --staged), and git aliases; a replacement option before git, whatever
    the subcommand (ls | xargs -I{} git log {}, echo main | xargs -I{} git rebase -x 'make test' {}), and
    a wrapper option cluster that holds I, J or i (ls | xargs env -i git log); git named in a quoted shell
    line (ls | parallel 'git log --oneline {}', xargs sh -c 'git -C "$d" status'); a later word git
    after an allowed form (ls | xargs git log --grep git); a git word that is only an argument or a
    value, with no listed subcommand after it (ls | xargs grep -l git, find . -name '*.md' -exec grep -l
    git {} +, fd -e md -X grep -l git, ls | parallel echo git restore, ls | xargs echo git restore); an
    expansion followed by a subcommand name git ships outside the list (xargs "$MAKE" clean, xargs "$X"
    add); and text searches for git command text (git ls-files | xargs grep -n 'git checkout', fd -e md
    -X rg 'git reset', ls | xargs rg 'git restore'). Writing the search pattern so that git is not a
    whole piece (grep -l 'gi[t]') or running git directly avoids the refusal. Round 46 (qanorm45 F1,
    F2, F4) adds, as cannot-parse behind those programs, every command whose first word is not a listed
    plain program, so these ordinary commands are refused (58 rows moved from the allow corpus): a shell,
    su, flock, python3, ipython, perl, awk, sed, ssh, find, fd, uv or fish there (echo 'echo hi' | xargs
    sh -c, find . -exec sh -c 'wc -l "$1"' _ {} ';', ls | xargs -I{} sh -c 'echo {}', ls | xargs perl -ne
    'print if /TODO/', ls *.txt | xargs awk '{print FILENAME}', ls | xargs -I{} sed -n '1p' {},
    find . -name '*.py' -print0 | xargs -0 -I{} python3 -m py_compile {}, echo host1 | xargs -I{} ssh {}
    uptime, ls | xargs -I{} find {} -name '*.py' -exec wc -l {} +); a wrapper before a listed program
    (ls | xargs sudo wc -l, ls | xargs nice -n 5 wc -l, ls | xargs timeout 5 wc -l, ls | xargs sudo git
    status, printf 'FOO=1' | xargs env); a program not on the list (parallel gzip ::: a.log b.log, ls |
    parallel -j 4 gzip {}, sem -j 2 make test); a quoted shell line behind GNU parallel, sem or rush (ls |
    rush 'echo {}', parallel -j4 'echo {}' ::: a b c, and a shell there: printf 'make all' | parallel sh
    -c, parallel sh -c ::: 'make all'); no command behind GNU parallel, sem, xe or rush (the items are
    the commands it runs: parallel ::: 'make all'); a listed name that a
    replacement option may rewrite (ls | xargs -I gr grep x); and, outside the corpus, a setting name as
    a word anywhere in such a command (ls | xargs grep -l GIT_DIR, ls | xargs grep PATH notes.txt). Running
    the command directly, a listed program behind the path-adding program (ls | xargs wc -l), or a loop
    over the items (for f in *; do ...; done) avoids the refusal. (Round 42's
    table, PATH_APPENDERS, recalled from each
    tool's documentation and not witnessed, decides where _parallel_runs_code reads the command
    word of the round 28 class, and from round 46 where _appended_parallel_start finds the command word
    (strictly: an option it does not settle is cannot-parse there); an error in it can still move that
    word either way: a value option
    listed as a flag would make its value the command word, and a flag listed as taking a value would
    hide the word after it.) A command word the guard has no rule for (chronic, chroot, watch, pdsh, a
    script) is read only by the unknown-command scan: it denies as cannot-parse when a later unquoted
    word is a removal command name, git with a form the git rule refuses as written (chroot / git restore
    --ours f), cargo or rsync with a denied form, or a shell, interpreter, find, fd, xargs or other
    wrapper the guard knows whose own check finds something (ls | chroot / xargs git restore --ours);
    what passes is a path or item such a program adds to the git command it runs (ls | foo git restore
    --ours), GNU parallel, sem, xe or rush behind it, a command in a quoted word (foo 'git restore --ours
    f'; the broad layer still refuses one whose text holds a removal word or a round 15 removal form),
    and whatever the program runs that its words do not name;
    (round 43, qanorm42 N2) an operation ref on the right of the merge-base form A...B (git checkout
    HEAD...MERGE_HEAD -- f, which by git-checkout(1) reads the merge base of HEAD and MERGE_HEAD, stage 1
    in a conflicted merge; inferred, not witnessed), as in rounds 41 and 42;
    (round 38, qanorm37 F1) git rebase, am, merge, cherry-pick and revert --quit, each also as an
    abbreviation: left allowed because, by git's documentation (inferred, not witnessed), --quit only
    forgets the operation's state and leaves HEAD, the index and the working tree, a conflict resolution
    in progress included, as they are (see GIT_ABANDON_OPTIONS for the derivation); a command that
    git runs from configuration (git -c core.pager=..., core.editor, core.sshCommand, sequence.editor,
    diff.external, a ! alias; the broad layer refuses one whose text holds a removal word, and from
    round 34 a git -c or git config in a command removes every exception) and a git subcommand that runs a command and is not named in WHAT IT DENIES; and the dashed programs
    (/usr/lib/git-core/git-rm, git-clean and the like); git help.autocorrect set in a configuration file
    (by an earlier command or by hand), by GIT_CONFIG_COUNT and GIT_CONFIG_KEY_n or
    GIT_CONFIG_PARAMETERS, or by a -c value built at run time: with it, git runs a mistyped subcommand
    as the one it takes the word for (git cleam -fd may run git clean -fd; qanorm20 reports git lgo
    running git log under it), and round 21 denies that only when the git argv holds a removal word or a
    round 15 removal form, which a typo such as cleam does not;
  * python attribute chains to an os module it does not track (shutil.os.remove, sys.modules["os"].remove);
  * removal outside Bash (other tools, MCP servers, processes it never sees);
  * hook failure or timeout (a hook that is not registered, not run, or stopped by the platform's timeout
    decides nothing; its own errors and its own deadline deny); (round 30, qanorm29 F4) the internal
    deadline is a SIGALRM, whose handler Python runs only between bytecode instructions, so it cannot
    interrupt one long C-level call (a regular expression match, for example), which runs on until the
    platform's timeout and so fails open as above (inference, not witnessed: qanorm29 found no input that
    came close, at worst 0.63 s in process and 0.78 s end to end);
  * (round 32, D-2385, D-2384) through the broad layer's exceptions. Round 35 (see BROAD LAYER, its
    Round 35 paragraph, which narrows the exception list given before it) exempts text only in a command
    that is, as a whole, one simple command of an allowlisted form (git [-C DIR] [-P | --no-pager]
    commit, gh pr or gh issue create, edit or comment, grep, or rg, each with only the options its
    allowlist names and with the command word exactly git, gh, grep or rg as written), and only this text
    in it: the git commit message (the value of -m, --message, -F or --file), the gh body (the value of
    -b, --body, -F or --body-file), the grep or rg patterns, and the body of the one top-level
    here-document with a plain delimiter that git commit -F - (or --file=-) or gh -F - (or --body-file -)
    reads. Every other command gets no exception, and its whole text is read: a second command, an
    operator (pipeline, ;, &&, ||, &, newline list, subshell, group or compound command), any other
    redirection, a NAME=VALUE word, a $, backquote, <( or >( outside the exempt text, or an option the
    allowlist does not name removes every exception. So no program that the same command starts can run
    the exempt text and pass: git commit -m 'rm -rf x' && ruby -e "$(git log -1 --format=%B)", git
    commit -m 'rm -rf x'; node .git/COMMIT_EDITMSG, git commit -m 'rm -rf x'; make -f
    .git/COMMIT_EDITMSG, a hook, a PATH binding or a function named git written before git commit -m
    'rm -rf x', and rg --pre=sh 'rm -rf x' f each get the broad-refusal verdict, as each text holds rm
    outside any exemption. What remains, and passes:
    - a removal word only in that exempt text, run by a program that configuration or files outside the
      command choose (the inner layer cannot see them): a git hook (pre-commit, commit-msg; git commit
      with -m and no editor option still runs them, and they read the message file) or core.hooksPath,
      core.editor, GIT_EDITOR or gpg.program set in a repository, user or system configuration, the
      environment or the hooks directory (by git's documentation, not witnessed: git commit with no -m
      or -F, or --amend with neither and without --no-edit, starts the editor), -C DIR naming a
      repository whose configuration sets one of those, a gh alias, extension or editor set outside the
      command, an rg configuration file named by RIPGREP_CONFIG_PATH set before the command, and git,
      gh, grep or rg reached through a PATH set before the command (in the environment or by an earlier
      command), an alias, a hash -p entry or a function defined outside the command;
    - a later, separate command (another tool call) that runs text an earlier command stored
      (.git/COMMIT_EDITMSG, git log output, gh issue view output), which no single-command test can see;
    - a removal that the inner layer misses and whose removal word sits only in exempt text that bash
      itself runs because this lexer reads the here-document differently: a body line the tracking
      misreads that holds a removal command behind a command word the command-position test does not
      name (chroot /srv rm x, mywrap rm x, ln -sf /bin/rm r; ./r, watch 'rm x') or behind a command
      word built at run time (R=rm; $R -rf x), and a git commit or gh here-document message inside
      "$( )" that bash ends at a line this guard does not treat as the end (qanorm32 F1 witnessed bash
      5.3.9 ending it, and the substitution, at a body line EOF)", then running the next line); round 33
      drops the exemption for any body line that starts with the delimiter after leading spaces or tabs,
      and that bash ends it at no other line is inference, not witnessed (round 33 witnessed, with echo
      only, that bash 5.3.9 does not end a here-document inside a ( ) subshell at an EOF) line);
    - a removal word in another letter case: it is matched case-sensitively, as bash command names are,
      so Remove or RM in text passes the broad layer; and the broad layer reads text only, so a removal
      built at run time (r$EMPTYm) or held in a variable passes it as it passes the inner layer;
  * and file permissions remain the real boundary.
  Round 34 (qanorm33 N6): the inner layer does not catch the forms in the rest of this list, but each
  example given here whose text holds a removal word or a round 15 removal form as written (chroot /srv
  'rm' x, watch 'rm x', script -c 'rm x', nix-shell -p hello --run 'rm x', tar --to-command='rm x' -xf
  a.tar, echo 'rm x' | chroot /srv 'sh', git checkout -f main, git -c core.editor='rm -rf x', git config
  alias.x 'rm -f', shutil.os.remove, gvfs-rm x, python3.7m -c with os.remove) is refused by the broad
  layer; each passes only when its removal word sits in exempt text or is built at run time.
  Also not caught, beyond that list: wrappers it does not know (for example chroot, watch,
  script, uvx, uv tool run, nix-shell --run, tar --to-command), whose command word it does not look
  past, when the removal command name is quoted, part of a string or built at run time, or the removal
  is another form that no later unquoted shell, su, interpreter, find, fd, ssh, eval or known wrapper
  word starts (chroot /srv 'rm' x, watch 'rm x', script -c 'rm x', nix-shell -p
  hello --run 'rm x', tar --to-command='rm x' -xf a.tar): the round 16 fail-safe reads only an unquoted
  removal command name or git, cargo or rsync (round 23) and a removal form, and round 20 adds the full
  argv check from those later words only; (qanorm27 N3) so a quoted or escaped runner word (a shell,
  su, interpreter, find, fd, ssh, eval or known wrapper name) after such a wrapper is not read as one
  either, also behind xargs (echo 'rm x' | chroot /srv 'sh', printf 'rm x' | xargs -0 chroot /srv 'sh'
  -c '$0', the same with "bash" or s\\h), though round 28 does read quoted words of a GNU parallel, sem,
  xe or rush command, and round 29 their quotes, backslashes and quoted removal command names (parallel
  'rm x' ::: a is denied; see the xargs item above); an awk or sed program that runs a command another way (awk's printf to a pipe through a
  variable, sed's w /dev/stdout fed to a shell), or whose removal is built at run time, read from a
  file, or held in a variable that an earlier command set (export C='rm x'; awk 'BEGIN{system(ENVIRON["C"])}');
  uv run -m, -s,
  --module, --script or --gui-script, which runs a module or a script file; an rsync
  or cargo option or subcommand built at run time (rsync $OPTS src/ dst/, cargo $SUB); a git clean,
  git stash or cargo clean form behind a git or cargo alias; other deletion programs it does not name,
  including programs that delete their input file (gzip big.log, zip -m a.zip f), gvfs-rm, the legacy
  name of gio remove, and (round 48, named with what each loses in the round 48 item above) package
  uninstallers (pip uninstall, npm uninstall, cargo uninstall), git apply, git am and patch with a diff
  that deletes a file, git sparse-checkout set, git stash drop, git stash clear and git gc --prune=now;
  python names with an m suffix (python3.6m, python3.7m), which it does not count as
  python;
  a script run with source or '.'; and a quoted or partly quoted expansion in a find option value, or an
  expansion in a find option word, that splits into several words or none ($E"x" with E='a b', -$OPT).
  Denied in the safe direction although nothing is removed: a --rm flag in a command it cannot parse; any
  removal word in a command it cannot parse, for example case inside $( ), which it does not
  model (x=$(case $1 in -h) echo remove;; esac)), and (round 22) any round 15 removal form there, even a
  dry run (coproc NAME { echo hi; }; git clean -n); any here-string, quoted or not, in a command whose
  text holds a removal word anywhere (cat <<< 'rm x'); (round 32) any here-document whose body holds a
  removal command in command position, even a commit message body (a line that starts rm, or git rm
  ..., in git commit -F - <<'EOF' or git commit -m "$(cat <<'EOF' ...)"); and any removal word, even a quoted argument or a --rm flag, in a
  command that holds one of the constructs it cannot read exactly (for example echo rm after
  mapfile -t lines, or a quoted string inside (( )) next to git rm, trap 'echo rm' EXIT, echo $"hi"; git
  rm x, or systemctl enable x next to docker run --rm); a here-string or an arithmetic << shift in a
  command with a line continuation, which the here-document test also matches; a backslash-newline
  right after a word or operator next to any removal word (echo rm\\ then a newline and x, ls &&\\ then a
  newline and git rm x), which the line-continuation test also matches; sudo -l followed by
  a removal command, which only lists; any $ directly before a quote, which the dollar-quote test also
  matches, such as a regex $ anchor before a closing quote (grep 'remove$' f) or a quoted $ field
  separator (awk -F'$' '{print $2}' f | grep remove), and a word with S in an option cluster anywhere after an env word
  (env LC_ALL=C ls -lS && git rm x), which the env -S test also matches; a command word built at run
  time next to any removal word ("$GIT" rm x, $SUDO apt-get remove x); a [ test whose words hold a
  removal word ([ "$1" = remove ] && echo yes, [ -f rm-list.txt ] && cat rm-list.txt,
  if [ -e notes.rm ]; then echo y; fi), because [ counts as a glob character and so the [ builtin as a
  command word built at run time (test "$1" = remove is allowed); fd -tx rm, whose -tx cluster the
  attached fd exec option test reads as -x; and a find or fd option it does not know before an exec
  option, next to a later removal word (find -O3 . -exec grep -l rm {} +); and an expansion or glob in
  a find exec block before a later removal word (find . -exec grep -l "$PAT" {} + -o -name rm-list), or
  an unquoted one in a find option value before a later exec option and removal word; the word getattr,
  even in a quoted string, a comment or an argument (python3 -c 'print(getattr(o, "name"))', echo
  getattr), and a removal word that appears only after NFKC folding (rm written in fullwidth letters,
  U+FF52 U+FF4D, as an echo argument), in a command it cannot parse or that holds a here-document, a
  here-string or another construct it cannot read exactly; and any .unlink, .rmdir, .removedirs or
  .rmtree attribute in a python -c program, whatever its object (r.unlink("k") on a Redis client
  deletes a key, not a file), and getattr with one of those names on any object. Also git rm -f in a dry
  run (git rm -n -f), git rm --force followed by --no-force, and git rm -f with an abbreviated --cached
  (--cach), all denied; git rm with an expansion before -- (git rm "$f", git rm $(git ls-files -d)),
  denied as cannot-parse because the expansion may become -f, --force or --no-cached (git rm -- "$f" is
  allowed); and a git option it does not know, or an expansion, before the git subcommand, in an argv
  that holds a removal word (git --html-path rm x, git $OPTS rm x), denied as cannot-parse. Round 15
  adds these over-denies: a python -c program that names subprocess, system or popen and holds any
  removal word, even one that removes no file (subprocess.run(['kubectl', 'delete', 'pod', 'x'])); a
  perl -e program with the word unlink or rmtree anywhere, even in a string (perl -e 'print "unlink"');
  rsync --delete in a dry run (rsync -n --delete); git clean -n with an expansion before -- (git clean
  -n "$d"; write git clean -n -- "$d" instead) or with any later --no- option, denied because the
  expansion or option may turn the dry run off; git worktree remove with an expansion before -- (git
  worktree remove "$wt"), denied as cannot-parse because the expansion may become -f; git stash -u with
  a later --no-include-untracked; cargo clean --dry-run, and cargo with an option it does not know or an
  expansion before the subcommand and a later clean word (cargo -Zunstable-options run -- clean); a -c
  string of sh, dash or zsh that bash reads differently, checked as bash; and flock -c STRING FILE (the
  -c before the file, which flock may reject), where -c is an option the guard does not know, denied as
  cannot-parse when a removal word follows. The grep over-deny above (grep 'remove$' f, from the dollar-quote
  test) stays: narrowing that raw-text test would rest on the lexer's reading of quotes, which the
  raw-text test exists to back up. Round 16 adds these over-denies: the commands listed under FAIL-SAFE
  (an unquoted removal command name after a command word it has no rule for, such as grep rm file or
  docker rm container); a python or perl shell call whose text holds the words of a round 15 removal
  form anywhere, in any order, even split over calls or strings (os.system('git status');
  print('clean')) (git checkout -f or git switch -f of a branch run that way,
  os.system('git checkout -f main'), is denied too, but that is not an over-deny: both throw away local
  changes to tracked files, as RESIDUAL and WHAT IT DENIES say); a perl program with a shell call and any removal word
  (perl -e 'system("ls"); print "rm"'); a shell -c string it cannot parse that holds those words; a git
  abbreviation that git rejects as ambiguous (git switch --d main, git rebase --e 'rm x' main) read as the
  option it may abbreviate; a git option value read as a command string when it names a program path
  (git difftool -x rm); and pipx run rm x, which runs the PyPI app named rm. Round 17 adds these
  over-denies: git checkout -f of an operand built at run time that names a branch (git checkout -f
  "$BRANCH") or of an expansion that becomes an option (git checkout -f $OPT main); a fish word after
  the script operand read as -c, -C, --command or --init-command (fish script.fish -C 'rm x', which
  passes those words to the script); an ipython program that ast cannot parse and whose text holds the
  words of a round 15 removal form anywhere (ipython -c 'print("git clean") ; %time 1'); and an ipython
  program that names get_ipython and holds a removal word or form anywhere, even in a string.
  Round 54 (grc review of rounds 51 to 53): a hook payload that starts with a UTF-8 byte order mark is
  denied as malformed input (fail closed) even when the rest would be allowed, on input the hook harness
  does not send, and the guard keeps that deny rather than strip the mark, so it accepts nothing more
  (a fail-closed row of the self-test pins it).
  Round 18 (qanorm17) adds these denies: a process substitution inside an array assignment NAME=( ... )
  is walked as a command; a shell (bash, sh and the rest above), at, batch, python or perl, also behind
  the wrappers it knows, that reads its program from stdin (no -c, -e, -m or script operand, or sh -s, or
  -) in a pipeline whose text holds a removal word or a round 15 removal form anywhere (echo 'rm x' | sh,
  ls | sed 's/^/rm /' | bash), or from a process substitution (bash <(...), at -f <(...)) whose text holds
  one, denies as cannot-parse (round 19 replaced the pipeline split with the whole-command rule below); an
  ipython option without = takes a next word that does not start with - as its value (--profile foo);
  git checkout -f or --force with no operand, git submodule deinit -f or --force, git read-tree with -u
  and --reset, and git checkout-index -f or --force deny (an expansion before -- that may become the
  option denies as cannot-parse); a shell -c string that names "$@", $*, $0 to $9 (also in braces), a
  python -c program that names argv and a perl -e program that names ARGV have their later words read as
  a command (from the word each reference names), and an unquoted removal command name or git with a
  removal form among those words denies as cannot-parse, as for a command word it does not know; an eval
  string (also builtin eval) is checked as a command string, as a trap action is; an expansion that may
  become -c before a round 15 removal form denies for every shell, as for su; su and fish long options
  are read with the abbreviations they accept (an ambiguous one that may be a command option is read as
  one); an ipython line whose first word is the rm or rmdir shell alias (also %rm), other than an
  assignment, is checked as a shell command; git checkout -f of an operand that starts with : (pathspec
  magic) or ~ denies; and past the depth cap the word getattr, NFKC folding and the decoding above count
  as a removal word. Over-denies this adds: any such pipeline with a removal word or form anywhere in
  it, even where the program reads no such text (cat rm-list.txt | xargs -n1 sh, whose sh reads the
  script files it is given), and an rm or rmdir line in an ipython string that spans lines; a later word read as a command that
  is only data (sh -c 'echo "$@"' _ rm x); git submodule deinit and git checkout-index with an expansion
  before -- ; git checkout -f -b NEW and git checkout -f --orphan NEW with no start point.
  Round 19 (qanorm18) makes the stdin-program rule structural: a shell, at, batch, python, perl, source
  or . that reads its program from its standard input or from a process substitution, /dev/stdin,
  /dev/fd/N, /proc/PID/fd/N or - (or an expansion where its program operand is), wherever it is in the
  command, denies as cannot-parse when the command feeds a standard input or file descriptor anywhere (a
  pipe on one line or continued, <, <>, <&, a here-document or here-string, <( ), >( ) or coproc) and its
  text holds a removal word or a round 15 removal form anywhere; so do sh < <(...), bash 0< <(...),
  echo ... > >(sh), echo ... | tee >(sh), { sh; } < <(...), exec < <(...); sh, sh <&3, echo ... | bash
  /dev/stdin, source <(...) and . <(...). A shell -c string that runs such a reader (sh -c 'cat | sh')
  counts as reading the outer shell's input. A command it cannot parse that names a reader and holds a
  round 15 removal form also denies as cannot-parse. The text tests for round 15 forms also read git
  checkout-index -f, git submodule deinit -f and git read-tree -u --reset (in a python or perl shell
  call, a shell -c string it cannot parse, a program read from stdin and past the depth cap). A shell -c
  string's for or select NAME with no in list, ${!#} and BASH_ARGV, python's sys.orig_argv, and perl's
  shift and pop count as running later arguments (any later word for the first three), and ipython
  --c PROGRAM (also --c=PROGRAM) is read as -c; that IPython accepts --c is inference from the traitlets
  documentation, not witnessed. Over-denies this adds: a reader that reads a program from stdin, or from
  a file it is given by redirection, in any command that feeds an input and holds a removal word or form
  anywhere, even where the program holds none (sh < setup.sh && git commit -m 'remove x', sh < rm-list.sh,
  echo hi | sh; echo rm), and a reader with an expansion as its program operand in such a command
  (bash "$script" < in.txt; echo rm); a later word read as a command when a for loop with no in list,
  ${!#}, BASH_ARGV, shift or pop only uses it as data. Still not covered: a python -c or perl -e program
  that reads its program from stdin itself (exec(sys.stdin.read()), eval <STDIN>), a reader whose stdin
  is fed by a file descriptor the command did not open, and a file given to source or . that is a regular
  script file (see RESIDUAL).
  Round 20 (qanorm19, gemnorm19): a cannot-parse from the argv check of a program's later arguments now
  propagates (sh -c '"$@"' _ fd -xrm was allowed); su with no -c string, sudo -s, sudo -i and doas -s
  with no command, ssh with no remote command (and without -n, -N, -f, -W, -O, -G, -Q, -V or -s), and
  exec su read a program from stdin like any shell; when a program refers to its later arguments, any
  later word, quoted or not, that holds a removal word or a round 15 removal form denies as
  cannot-parse; a reader given a script operand, or a command word that is a path the command writes,
  in a command that writes a file (>, >>, >|, &>, &>>, >& FILE or tee, to a path other than /dev/null,
  /dev/zero, /dev/tty, /dev/stdout or /dev/stderr; round 29 also cp, mv, install, ln, dd of= and a
  python or perl program that may write) and
  holds a removal word or form denies as cannot-parse; a command word it does not know runs the full
  argv check from each later unquoted word that names a shell, su, an interpreter, find, fd, ssh, eval
  or a wrapper or runner it knows (bounded per command by a scan budget, past which a removal word or
  form in the rest of the argv denies as cannot-parse), and looks past itself to such a word for a
  reader of stdin (echo 'rm x' | chroot /srv sh); ssh with a remote command is checked as a shell
  command string; awk system() or a pipe, and sed e or s///e, with a removal word or form deny as
  cannot-parse; ipython's code_to_run and exec_lines config options (any class prefix, such as
  --InteractiveShellApp. or --TerminalIPythonApp.) are checked as programs, a list value line by line;
  git checkout -f with --theirs or --ours denies. That IPython reads those options, that ssh joins its
  remote words for the remote shell, that git checkout takes -2 and -3 for --ours and --theirs, and
  that sudo -s, sudo -i, doas -s and su read stdin, are inference from their documentation, not
  witnessed. Over-denies this adds: a later word that only holds data with a removal word
  (sh -c 'echo "$1"' _ 'remove me'); a reader or written path in a command that writes any file and holds
  a removal word anywhere (python3 build.py > out.log && git commit -m 'remove x'); ssh with no command
  that is fed any input with a removal word (cat rm-notes.txt | ssh host), and ssh host rm x, which
  removes on the remote host only; a word that names a shell, interpreter, find or wrapper after a
  command it does not know where it is only data, next to a removal (docker exec c sh -c 'rm /tmp/x',
  which removes in the container; cat rm-list | grep sh, where grep's pattern sh counts as a reader);
  an awk program whose | is regex alternation, and a sed script with a standalone e-word (such as me,
  ge or 1e) as data, next to a removal word (awk '/remove|delete/' f); a fed command whose sudo or doas
  has an option the guard does not know; and an unknown command nesting known wrappers past the depth
  cap next to any removal word.
  Round 21 (qanorm20): F1 to F4, as WHAT IT DENIES says (awk data words, wrapper long option
  abbreviations, git help.autocorrect and subcommands git does not ship, and rows for the enable, eval,
  hash, mawk and nawk entries). Over-denies this adds: an awk program that runs a command next to a -v
  value, operand or NAME=VALUE word that holds a removal word or form only as data (awk '{print | "sort"}'
  remove-list.txt); any git command that sets help.autocorrect, even with a known subcommand or a value
  that turns it off (git -c help.autocorrect=0 status), and git config that only reads it; a git alias
  or git-WORD program whose argv holds a removal word or form (git ci -m 'remove x', git lfs track
  '*.rm'), and a later git word of a command it does not know followed by such an argv (ls git rm-notes);
  and a long option abbreviation of a wrapper or runner that the program itself rejects (uv's and
  poetry's parsers may not accept abbreviations, and getopt_long rejects an ambiguous one), which is
  read on as the option it may abbreviate. That timeout, sudo, env, nice and the other wrappers accept
  these abbreviations is inference from getopt_long's documented behaviour, not witnessed.
  The set-aside folders are under /tmp, which a host may clear at reboot or by age (systemd-tmpfiles);
  if so, what is moved there can be deleted without a human. This guard does not check that. Another
  account (or a process under the same UID) can also create /tmp/grc or /tmp/deleteme-grc first, or
  place a symlink at either path, and so redirect what is moved there or keep it; the guard does not
  check that either.
  The self-test does not exercise the deadline, and its deny-logic flip switches the final verdict off,
  not each detector in turn, so it does not show which detector denies a row. Some detector entries
  have no row that fails when the entry alone is removed: the nt entry of the from-import modules (no
  row uses from nt import); the here-document operator pattern of the line-continuation test (the lexer
  also marks every here-document operator); and most entries of the find, fd, setsid, flock, taskset,
  uv, chrt, unshare, fakeroot, strace, ltrace, pipx and poetry option tables, of the perl and cargo
  option sets, of the short value letters in GIT_COMMAND_OPTIONS, and of the bash builtins the round
  16 fail-safe treats as inert. Removing one of those last ones changes only what is over-denied, not
  what gets through (a builtin taken off that list is read as a command word it does not know):
  without the pattern, a line continuation next to a
  << that is not an operator stops being denied; an option the guard no longer knows is read as an
  unknown option or a find primary, which denies more (for cargo, when a clean word follows). Round 15
  added rows for the rmdir and removedirs python names, read through getattr with a literal name and
  through a from-import, so removing either entry fails a row. Round 21 (qanorm20 F4) added rows that
  fail when the enable or eval entry of the string-evaluation builtins, the hash entry of alias, hash,
  mapfile and readarray, or the mawk or nawk entry of the awk names is removed alone.
  Round 32 adds a rule-revert group: each _RULE_CASES row passes with its _RULES entry (one exception of
  the broad layer, the here-document command-position test, or the here-document narrowing) and fails
  with that entry set to False; the self-test also checks that every allow row still passes the inner
  layer and pins how many of them the broad layer refuses. The entries of the grep and rg option tables
  and of the command-position runner names have no row of their own. Round 33 (qanorm32 F1 to F4) adds
  four _RULES entries to that group, each with rows that fail with the entry set to False: the
  here-document delimiter prefix, the here-document command words, the exact command word (with the
  PATH word test) and function shadowing. Round 34 (qanorm33 N1 to N4) adds five more, under the same
  test: PATH binding, git editor and configuration, exempt text runner, interpreter program expansion
  and runner readers; rows that two rules refuse are in the plain broad or cannot-parse groups.
"""

import ast
import json
import os
import re
import shlex
import signal
import subprocess
import sys

ALLOW = "allow"
DENY = "deny"
CANNOT_PARSE = "cannot-parse"
BROAD = "broad-refusal"
ERROR = "error"
MALFORMED = "malformed-input"

_REASONS = {
    BROAD: ("no-remove-guard: refused in the safe direction by the broad text layer. The parser found no "
            "removal in this Bash command, but its text holds a removal word (rm, rmdir, unlink, shred, "
            "srm, wipe, delete, remove, removedirs, rmtree or getattr, as written, after decoding and "
            "quote removal, or after NFKC folding) or a destructive git form (git clean, git reset "
            "--hard, git checkout -f and the like, also cargo clean and rsync --delete). Re-issue the "
            "command without that word, or write the text to a "
            "file with the Write tool and run git commit -F <file>. To remove files, move them into one "
            "of the set-aside folders, /tmp/grc/deleteme or /tmp/deleteme-grc, and leave the deletion "
            "to a human. This guard has no opt-out."),
    DENY: ("no-remove-guard: denied. This Bash command removes files (rm, rmdir, unlink, shred, srm, wipe, "
           "find -delete or -exec rm, git rm -f, git clean, git worktree remove -f, git reset --hard, "
           "git stash -u or -a, git checkout -f -- PATH or with no operand, git switch -f, git "
           "submodule deinit -f or update -f, git read-tree -u --reset, git checkout-index -f, git rebase, "
           "am, cherry-pick or revert --abort or --skip, git merge --abort, git checkout or restore -m, "
           "--merge, --conflict, --ours, --theirs, -2 or -3 of a path, or from MERGE_HEAD, "
           "CHERRY_PICK_HEAD, REVERT_HEAD, REBASE_HEAD, AUTO_MERGE or FETCH_HEAD (it overwrites a conflict "
           "resolution), a "
           "removal in git "
           "submodule foreach, git rebase --exec or git bisect run, rsync --delete or --remove-source-files, "
           "cargo clean, a removal in a bash, sh, dash, zsh, ksh, mksh, ash, fish, tcsh or su -c string "
           "or an ssh remote command, "
           "a perl -e unlink, rmtree or shell call with a removal, or "
           "a python -c os.remove, os.unlink, os.rmdir, os.removedirs, shutil.rmtree, Path.unlink, "
           "Path.rmdir, or a subprocess, os.system or os.popen call with a removal word or git clean, "
           "cargo clean and the like), and the grc "
           "main session does not remove files. "
           "Move what you want gone into one of the set-aside folders, /tmp/grc/deleteme or "
           "/tmp/deleteme-grc (mkdir -p the folder, then mv --backup=numbered PATH into it, which first "
           "renames an earlier discard of the same name to NAME.~N~ so that it is kept, not overwritten), "
           "and leave the deletion "
           "to a human. This guard has no opt-out."),
    CANNOT_PARSE: ("no-remove-guard: denied in the safe direction. The guard could not parse this Bash "
                   "command, or it holds a construct the guard cannot read exactly (a line continuation "
                   "inside a word, a removal command in command position in a here-document, a "
                   "here-string, a backquote inside double quotes "
                   "holding \\\", a NUL from $'...', a quote inside arithmetic, "
                   "a # inside an array assignment, an env -S escape, a NAME[ command word, alias, hash, "
                   "mapfile or readarray, an attached fd exec option, a command word built at run "
                   "time, a removal command name after a command word it does not know (grep rm f: "
                   "quote the word, grep 'rm' f), a ${ } or ${| } command "
                   "substitution, a $'...' or $\"...\" string, env -S, BASH_CMDS or BASH_ALIASES, a "
                   "string-evaluation builtin such as eval, trap or let, a shell or interpreter that reads "
                   "its program from standard input, /dev/stdin, /dev/fd/N or a process substitution "
                   "(also su, sudo -s or -i, doas -s or ssh with no command), a script written to a file "
                   "and run in the same command, an awk system() or sed e command, a shell or wrapper "
                   "after a command word it does not know, or "
                   "a program that runs its later arguments, such as sh -c '\"$@\"' _ rm x, or a command "
                   "nested past the depth cap), and its text holds a removal word "
                   "(rm, rmdir, unlink, shred, srm, wipe, delete, remove, removedirs or rmtree, as written, "
                   "after decoding and quote removal, or after NFKC folding as python folds names), a "
                   "removal form (git clean, git reset --hard, git checkout -f, cargo clean, rsync --delete "
                   "and the like) or the word getattr, so it cannot show that the command removes "
                   "nothing. Re-issue it in a plainer form the guard can parse, or move what you want gone "
                   "into one of the "
                   "set-aside folders, /tmp/grc/deleteme or /tmp/deleteme-grc, and leave the deletion to "
                   "a human. To pass text that holds a removal word (a commit message or a search "
                   "pattern), write the text to a file with the Write tool, then run git commit -F <file> "
                   "or grep -f <file>."),
    ERROR: ("no-remove-guard: denied in the safe direction. The guard hit an internal error, could not "
            "read the hook payload or ran past its deadline, so it could not evaluate this call. Move "
            "what you want gone into one of the set-aside folders, /tmp/grc/deleteme or "
            "/tmp/deleteme-grc, leave the deletion to a human, and report the guard failure."),
    MALFORMED: ("no-remove-guard: denied in the safe direction because the hook input was malformed. It "
                "was not UTF-8 JSON, was not a JSON object, had no string tool_name, or, for a Bash call, "
                "had no tool_input object or no string command, or a command that holds a NUL byte. The "
                "guard did not evaluate any command, so this says nothing about what the command does. "
                "Report the malformed hook input."),
}
_BANNERS = {
    BROAD: ("no-remove-guard refused a Bash call whose text holds a removal word or a destructive git form; "
            "use the set-aside folders /tmp/grc/deleteme or /tmp/deleteme-grc."),
    DENY: ("no-remove-guard denied a Bash call that removes files; use the set-aside folders "
           "/tmp/grc/deleteme or /tmp/deleteme-grc."),
    CANNOT_PARSE: ("no-remove-guard denied a Bash call it could not parse or read exactly that holds a "
                   "removal word (as written, after decoding and quote removal, or after NFKC folding), a "
                   "removal form such as git clean, or the word getattr; use the set-aside folders "
                   "/tmp/grc/deleteme or /tmp/deleteme-grc."),
    ERROR: ("no-remove-guard denied a Bash call after an internal error (fail-closed); use the set-aside "
            "folders /tmp/grc/deleteme or /tmp/deleteme-grc."),
    MALFORMED: "no-remove-guard denied a tool call whose hook input was malformed (fail-closed).",
}

# The self-test flips this to show that each deny and cannot-parse case is denied through this verdict
# switch, not by an internal error; it does not switch each detector off in turn (see the docstring).
# The hook never reads it from the environment, the payload or the command: there is no in-band opt-out.
_DENY_LOGIC_ON = True
# Round 32 (D-2385, D-2384): the broad layer's text-only exceptions and the narrowed here-document rule.
# The self-test reverts each entry in turn to show that its rows fail without it; like _DENY_LOGIC_ON,
# the hook never reads these from the environment, the payload or the command.
_RULES = {
    "git commit message": True,
    "gh body": True,
    "grep or rg pattern": True,
    "here-document command position": True,
    "here-document narrowing": True,
    # Round 33 (qanorm32 F1 to F4)
    "here-document delimiter prefix": True,
    "here-document command words": True,
    "exact command word": True,
    "function shadowing": True,
    # Round 34 (qanorm33 N1 to N4)
    "PATH binding": True,
    "git editor and configuration": True,
    "exempt text runner": True,
    "interpreter program expansion": True,
    "runner readers": True,
    # Round 35 (qanorm34 N2: B1, J1, J2, D1)
    "simple command allowlist": True,
}
DEADLINE_SECONDS = 5.0
MAX_CHECK_DEPTH = 32

REMOVERS = frozenset(("rm", "rmdir", "unlink", "shred", "srm", "wipe"))
PY_REMOVE_NAMES = frozenset(("remove", "unlink", "rmdir", "removedirs", "rmtree"))
PY_ALWAYS_REMOVE_ATTRS = frozenset(("unlink", "rmdir", "removedirs", "rmtree"))
PY_OS_MODULES = frozenset(("os", "posix", "nt"))
PY_FROM_MODULES = frozenset(("os", "posix", "nt", "shutil", "pathlib"))
FIND_EXEC = frozenset(("-exec", "-execdir", "-ok", "-okdir"))
# Round 42 (qanorm41 F5): gfind (GNU find as installed beside a BSD find, as gxargs is beside xargs) and bfs
# (a breadth-first find that takes find's primaries, and by its documentation -rm as a synonym of -delete;
# inferred, not witnessed) are read as find, at every place the guard names find
_FIND_NAMES = frozenset(("find", "gfind", "bfs"))
FD_EXEC = frozenset(("-x", "--exec", "-X", "--exec-batch"))
# Round 7: option words whose value is the next word (find: how many words), and option words that take
# none. Another word that starts with - may take a value, so after it a later exec word is ambiguous.
FIND_VALUE_OPTIONS = dict.fromkeys(
    ("-name", "-iname", "-path", "-ipath", "-wholename", "-iwholename", "-regex", "-iregex", "-lname",
     "-ilname", "-type", "-xtype", "-user", "-group", "-uid", "-gid", "-perm", "-size", "-newer", "-anewer",
     "-cnewer", "-samefile", "-inum", "-links", "-mtime", "-mmin", "-atime", "-amin", "-ctime", "-cmin",
     "-used", "-maxdepth", "-mindepth", "-fstype", "-context", "-regextype", "-fprint", "-fprint0", "-fls",
     "-printf", "-files0-from", "-D"), 1)
FIND_VALUE_OPTIONS["-fprintf"] = 2
FIND_PLAIN_OPTIONS = frozenset((
    "-print", "-print0", "-ls", "-prune", "-quit", "-true", "-false", "-empty", "-readable", "-writable",
    "-executable", "-nouser", "-nogroup", "-depth", "-d", "-mount", "-xdev", "-noleaf",
    "-ignore_readdir_race", "-noignore_readdir_race", "-daystart", "-follow", "-warn", "-nowarn", "-not",
    "-a", "-and", "-o", "-or", "-H", "-L", "-P", "-help", "--help", "-version", "--version", "-delete"))
FD_VALUE_LONG = frozenset((
    "--extension", "--type", "--max-depth", "--maxdepth", "--min-depth", "--exact-depth", "--exclude",
    "--ignore-file", "--color", "--threads", "--size", "--changed-within", "--change-newer-than", "--newer",
    "--changed-before", "--change-older-than", "--older", "--owner", "--base-directory", "--path-separator",
    "--search-path", "--max-results", "--format", "--batch-size", "--max-buffer-time", "--and"))
FD_PLAIN_LONG = frozenset((
    "--hidden", "--no-hidden", "--no-ignore", "--ignore", "--no-ignore-vcs", "--ignore-vcs",
    "--no-ignore-parent", "--no-global-ignore-file", "--no-require-git", "--require-git", "--unrestricted",
    "--case-sensitive", "--ignore-case", "--glob", "--regex", "--fixed-strings", "--absolute-path",
    "--relative-path", "--list-details", "--follow", "--no-follow", "--full-path", "--print0", "--quiet",
    "--show-errors", "--one-file-system", "--prune", "--strip-cwd-prefix", "--hyperlink", "--help",
    "--version"))
FD_VALUE_SHORT = "cdeEjoSt"
FD_PLAIN_SHORT = "01aFgHhiIlLpqsuV"
# Round 13: git options before the subcommand that take the next word as their value (or one joined with
# =), and ones that take none. Another word that starts with - may take a value, so the subcommand is
# unknown after it.
GIT_VALUE_OPTIONS = frozenset(("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env",
                               "--super-prefix", "--attr-source"))
GIT_PLAIN_OPTIONS = frozenset(("-p", "-P", "--paginate", "--no-pager", "--bare", "--no-replace-objects",
                               "--literal-pathspecs", "--no-literal-pathspecs", "--glob-pathspecs",
                               "--noglob-pathspecs", "--icase-pathspecs", "--no-optional-locks",
                               "--no-advice", "--exec-path", "--no-lazy-fetch"))
# Round 21 (qanorm20 F3): the subcommands git ships (git --list-cmds=builtins,main,nohelpers, plus the
# ones packaged apart). git runs any other word as an alias or a git-WORD program, or, when
# help.autocorrect is set, as the subcommand it takes the word for (git cleen -fdx runs git clean -fdx).
GIT_SUBCOMMANDS = frozenset((
    "add", "am", "annotate", "apply", "archimport", "archive", "backfill", "bisect", "blame", "branch",
    "bugreport", "bundle", "cat-file", "check-attr", "check-ignore", "check-mailmap", "check-ref-format",
    "checkout", "checkout-index", "cherry", "cherry-pick", "citool", "clean", "clone", "column", "commit",
    "commit-graph", "commit-tree", "config", "count-objects", "credential", "credential-cache",
    "credential-store", "cvsexportcommit", "cvsimport", "cvsserver", "daemon", "describe", "diagnose", "diff",
    "diff-files", "diff-index", "diff-pairs", "diff-tree", "difftool", "fast-export", "fast-import", "fetch",
    "fetch-pack", "filter-branch", "fmt-merge-msg", "for-each-ref", "for-each-repo", "format-patch", "fsck",
    "fsck-objects", "fsmonitor--daemon", "gc", "get-tar-commit-id", "grep", "gui", "hash-object", "help",
    "hook", "http-backend", "http-fetch", "http-push", "imap-send", "index-pack", "init", "init-db",
    "instaweb", "interpret-trailers", "last-modified", "log", "ls-files", "ls-remote", "ls-tree", "mailinfo",
    "mailsplit", "maintenance", "merge", "merge-base", "merge-file", "merge-index", "merge-octopus",
    "merge-one-file", "merge-ours", "merge-recursive", "merge-recursive-ours", "merge-recursive-theirs",
    "merge-resolve", "merge-subtree", "merge-tree", "mergetool", "mktag", "mktree", "multi-pack-index", "mv",
    "name-rev", "notes", "p4", "pack-objects", "pack-redundant", "pack-refs", "patch-id", "pickaxe", "prune",
    "prune-packed", "pull", "push", "quiltimport", "range-diff", "read-tree", "rebase", "receive-pack",
    "reflog", "refs", "remote", "remote-ext", "remote-fd", "remote-ftp", "remote-ftps", "remote-http",
    "remote-https", "repack", "replace", "replay", "repo", "request-pull", "rerere", "reset", "restore",
    "rev-list", "rev-parse", "revert", "rm", "send-email", "send-pack", "shell", "shortlog", "show",
    "show-branch", "show-index", "show-ref", "sparse-checkout", "stage", "stash", "status", "stripspace",
    "submodule", "subtree", "svn", "switch", "symbolic-ref", "tag", "unpack-file", "unpack-objects",
    "update-index", "update-ref", "update-server-info", "upload-archive", "upload-pack", "var",
    "verify-commit", "verify-pack", "verify-tag", "version", "whatchanged", "worktree", "write-tree"))
# Round 15: shells whose -c string is checked as a command, with this bash grammar. Round 16 (qanorm15 B2,
# MD1): ksh, ksh93, mksh, ash (also as busybox ash), fish, tcsh and csh too; su -c is in _check_su.
SHELL_NAMES = frozenset(("bash", "sh", "dash", "zsh", "ksh", "ksh93", "mksh", "ash", "fish", "tcsh", "csh"))
SHELL_VALUE_LONG = frozenset(("--rcfile", "--init-file"))
SHELL_COMMAND_LONG = frozenset(("--command", "--init-command"))  # fish --command STRING, --command=STRING
# Round 16 (qanorm15 B1): bash builtins that never run an operand as a command. Any other command word the
# guard has no rule for may be a wrapper it does not know, so a later removal command name in its argv
# denies as cannot-parse (see FAIL-SAFE).
_INERT_BUILTINS = frozenset(("echo", "printf", ":", "true", "false", "test", "cd", "pwd", "pushd", "popd",
                             "dirs", "export", "declare", "typeset", "local", "readonly", "unset", "shift",
                             "return", "exit", "read", "set", "shopt", "umask", "ulimit", "wait",
                             "type", "help", "getopts", "times", "logout", "disown", "suspend", "kill",
                             "caller", "history"))
# Round 17 (qanorm16 F1): IPython syntax that runs a shell command: a ! or !! line (also NAME = !cmd), the
# %sx and %system line magics, and the %%bash, %%sh and %%script cell magics (%%sx, %%system and %%! too,
# in the safe direction), and the name get_ipython, which reaches its system and magic calls.
_IPY_ESCAPE_LINE = re.compile(r"[ \t]*(?:[A-Za-z_][A-Za-z0-9_]*(?:[ \t]*,[ \t]*[A-Za-z_][A-Za-z0-9_]*)*"
                              r"[ \t]*=[ \t]*(?=[!%]))?(?:(!!?)|%(sx|system)(?![A-Za-z0-9_])"
                              r"|%%(bash|sh|script|sx|system|!)(?![A-Za-z0-9_]))(.*)\Z")
_IPY_SHELL_CALL = re.compile(r"(?<![A-Za-z0-9_])(?:subprocess|system|popen|get_ipython)(?![A-Za-z0-9_])")
# Round 16 (qanorm15 M1): git subcommands with an option whose value git runs as a command: long options
# that take a value, long options whose value must be attached with =, short options that take a value
# (attached or the next word), short options whose value must be attached, and other short options that
# take a value (skipped). git also accepts an unambiguous abbreviation of a long option.
GIT_COMMAND_OPTIONS = {
    "rebase": (("--exec",), (), "x", "", "sXC"),
    "difftool": (("--extcmd",), (), "x", "", "t"),
    "filter-branch": (("--setup", "--tree-filter", "--index-filter", "--msg-filter", "--env-filter",
                       "--commit-filter", "--parent-filter", "--tag-name-filter"), (), "", "", ""),
    "clone": (("--upload-pack",), (), "u", "", "objc"),
    "fetch": (("--upload-pack",), (), "", "", "jo"),
    "pull": (("--upload-pack",), (), "", "", "jsXo"),
    "ls-remote": (("--upload-pack", "--exec"), (), "", "", "o"),
    "archive": (("--exec",), (), "", "", "o"),
    "push": (("--receive-pack", "--exec"), (), "", "", "o"),
    "send-email": (("--sendmail-cmd", "--to-cmd", "--cc-cmd", "--header-cmd"), (), "", "", ""),
    "grep": ((), ("--open-files-in-pager",), "", "O", "efABC"),
}
# Round 31 (qanorm30 MINOR-1): git subcommand options that reset working-tree files to a commit, as git
# reset --hard does (inference from git's documentation, not witnessed); git also accepts an abbreviation.
# Round 37 (grc round 36 LOW): git merge --abort and git cherry-pick --abort too (each resets to the
# pre-operation state through git reset --merge, so it can throw away local changes and remove working-tree
# files the operation added; inference from git's documentation, not witnessed).
# Round 38 (qanorm37 F1): the set is derived as a class from git's own action-option lists, so that a
# reviewer can check it is whole. The five git commands that stop part-way and leave an operation in
# progress, and the in-progress actions each accepts (git 2.53: OPT_CMDMODE entries in builtin/rebase.c,
# builtin/am.c and builtin/revert.c, the last shared by cherry-pick and revert, and the --abort, --quit and
# --continue options of builtin/merge.c; read from git's source and documentation, since git <sub> -h was
# refused in this round, and checkable with git rebase -h, git am -h, git merge -h, git cherry-pick -h and
# git revert -h; no --abort or --skip has a short option, and the one short option among these actions,
# am's -r for --continue, resets nothing; round 39, qanorm38 F2):
#   rebase       --continue --skip --abort --quit --edit-todo --show-current-patch
#   am           --continue (--resolved, -r) --skip --abort --quit --show-current-patch --allow-empty
#   merge        --continue --abort --quit
#   cherry-pick  --continue --skip --abort --quit
#   revert       --continue --skip --abort --quit
# An action resets work when it rewrites the index and working tree to a commit: --abort (back to the
# state before the operation) and --skip (back to HEAD, dropping the current commit or patch), each through
# git's reset --merge or --hard. qanorm37 witnessed (git 2.53.0) that git revert --abort, revert --skip,
# cherry-pick --skip and am --skip discard a hand-made conflict resolution, as merge and cherry-pick --abort
# do, and that cherry-pick --skip and am --skip also remove a file the operation added (round 39, qanorm38
# F3: its revert test added no file, so that removal was not witnessed for revert). --quit forgets the operation's state and leaves HEAD, the
# index and the working tree as they are; --continue, --edit-todo, --show-current-patch and --allow-empty
# go on or show and reset nothing (inference from git's documentation, not witnessed): they stay allowed,
# and RESIDUAL names --quit. So every --abort and --skip of the five is denied, each also as an
# abbreviation (git accepts any unambiguous prefix; an ambiguous one such as --s is denied too, the safe
# direction, though git itself rejects it), and no --quit is.
GIT_ABANDON_OPTIONS = {"rebase": ("--abort", "--skip"), "am": ("--abort", "--skip"), "merge": ("--abort",),
                       "cherry-pick": ("--abort", "--skip"), "revert": ("--abort", "--skip")}
# Round 39 (qanorm38 F1): the per-path options of git checkout and git restore that rewrite a conflicted
# path from the index stages, derived as a class from git's own option lists (git 2.53.0, git checkout -h
# and git restore -h, run in this round). Every option in those lists, and what it does to a named path:
#   both     -m, --[no-]merge           recreate the conflicted merge from stages 1-3     STAGE REWRITE
#   both     --[no-]conflict <style>    the same as --merge, with that conflict style      STAGE REWRITE
#   both     -2, --ours                 write stage 2 to the working tree                  STAGE REWRITE
#   both     -3, --theirs               write stage 3 to the working tree                  STAGE REWRITE
#   both     -p, --[no-]patch           select hunks interactively (git checkout -p -- f, with no input,
#                                       left an unmerged f as it was; git restore -p not witnessed)
#   both     -q, --progress, --recurse-submodules, --overlay, --ignore-skip-worktree-bits,
#            --pathspec-from-file, --pathspec-file-nul, -U, --inter-hunk-context: read no stage
#   restore  -s, --source <tree-ish>    from a tree, not the index stages (see RESIDUAL)
#   restore  -S, --staged, -W, --worktree: the target; --ignore-unmerged skips an unmerged path (it warned
#            and left it as it was)
#   checkout -f, --force                denied since round 15 for a path (by git's documentation it
#                                       ignores unmerged entries; not witnessed)
#   checkout -b, -B, -l, --guess, -d, -t, --orphan, --overwrite-ignore, --ignore-other-worktrees: the
#            branch form; a TREE-ISH operand reads a tree, not the index stages (see RESIDUAL)
# Witnessed (git 2.53.0, throwaway repos, a merge conflict on f resolved by hand): git checkout -2 -- f,
# -3 f, --th f and --ou -- f, and git restore -2 f, -3 f, --t f and --ou f overwrite an unstaged resolution
# with stage 2 or 3; git checkout --m -- f, --conf=diff3 -- f and --c=merge -- f, and git restore --m f,
# --conf=zdiff3 f and -Wm f turn a staged resolution back into three unmerged entries and conflict markers;
# git checkout -- f and git restore f refuse (path is unmerged); git restore --ours, git restore --merge
# and git checkout --ours with no path refuse to run; a later --no-merge cancelled -m, --merge and
# --conflict=diff3 (the guard still denies those, the safe direction); git checkout -m f, --merge f and
# --conflict=diff3 f, with one operand and no --, recreated the conflict as the -- forms did. So each
# STAGE REWRITE option is denied for a named path, also as an abbreviation that git accepts (--m and --c in both; --th and --ou in
# checkout, which also has --track and --orphan; --t and --ou in restore) and in a short-option cluster.
GIT_STAGE_REWRITE_OPTIONS = {"checkout": ("-m", "--merge", "--conflict", "-2", "--ours", "-3", "--theirs"),
                             "restore": ("-m", "--merge", "--conflict", "-2", "--ours", "-3", "--theirs")}
# Round 40 (qanorm39 F1): every long option of git checkout and git restore, from the round 39 table above
# (git checkout -h and git restore -h were refused in round 40, so this list is not re-derived from them
# and no witness was run; checkable with git checkout -h and git restore -h). git's parse-options takes a
# word that equals a long option as that option, and a prefix of exactly one long option as that option
# (an abbreviation); a prefix of several is an error and git runs nothing. _git_long_names reads every long
# option word of both commands through this one table, so each abbreviation git accepts is matched: with
# this list, --m to --merge, --c to --conflict, --th to --theirs (checkout; --t also abbreviates --track)
# or --t to --theirs (restore), --ou to --ours (--o also abbreviates --orphan, --overlay and
# --overwrite-ignore in checkout, --overlay in restore), --pathspec-fr to --pathspec-from-file
# (--pathspec-f also abbreviates --pathspec-file-nul), --f to --force, --or to --orphan, --so to --source
# (restore), --u to --unified and --in to --inter-hunk-context. A prefix of several options is read as all
# of them: the safe direction, for a command git refuses to run. An option missing from this list can only
# make a prefix git refuses look unique, never the reverse.
GIT_PATH_COMMAND_LONGS = {
    "checkout": ("--quiet", "--recurse-submodules", "--progress", "--merge", "--conflict", "--detach",
                 "--track", "--force", "--orphan", "--overwrite-ignore", "--ignore-other-worktrees", "--guess",
                 "--ours", "--theirs", "--patch", "--ignore-skip-worktree-bits", "--pathspec-from-file",
                 "--pathspec-file-nul", "--overlay", "--unified", "--inter-hunk-context"),
    "restore": ("--source", "--staged", "--worktree", "--ignore-unmerged", "--overlay", "--quiet",
                "--recurse-submodules", "--progress", "--merge", "--conflict", "--ours", "--theirs", "--patch",
                "--ignore-skip-worktree-bits", "--pathspec-from-file", "--pathspec-file-nul", "--unified",
                "--inter-hunk-context")}
# The long options among them that take the next word as their value when written without =
GIT_PATH_VALUE_LONGS = frozenset(("--conflict", "--orphan", "--source", "--pathspec-from-file", "--unified",
                                  "--inter-hunk-context"))
# Round 40 (qanorm39 F3): the refs a merge, cherry-pick, revert or rebase writes while it is in progress
# (AUTO_MERGE: the tree of git's own merge result, with conflict markers). Round 41 (qanorm40 N3): they
# exist mostly, not only, while an operation stops on a conflict: MERGE_HEAD also after git merge
# --no-commit, REBASE_HEAD also when a rebase stops at an edit step (by git's documentation, inferred and
# not witnessed). By git's documentation (inferred, not witnessed) MERGE_HEAD and CHERRY_PICK_HEAD hold
# the commit whose version is stage 3 of a conflicted path, so git checkout MERGE_HEAD -- f and git restore
# --source=MERGE_HEAD f write what --theirs writes; (round 41, qanorm40 N2) REVERT_HEAD holds the reverted
# commit, whose version is the merge base, stage 1 (a revert of C merges with C as the base and C's parent
# as theirs), so a source of REVERT_HEAD writes the base version. Each overwrites a hand resolution. As a
# tree source of a named path they are denied; HEAD and other trees are not (see RESIDUAL). Round 41
# (qanorm40 N4): also FETCH_HEAD (in a git pull conflict it names the commit MERGE_HEAD names; inferred),
# the per-worktree spellings main-worktree/REF and worktrees/NAME/REF (by git-worktree's documentation,
# inferred), and any letter case (on a case-insensitive file system merge_head may resolve; not verified).
# ORIG_HEAD is not among them: during a merge it names HEAD's commit (stage 2, as HEAD, which stays
# allowed), and git checkout ORIG_HEAD -- f is a routine recovery after git reset (see RESIDUAL).
# Round 42 (qanorm41 F2): the match is the ref name itself, ending the word or followed only by a revision
# suffix (~, ^, @ or :, as in MERGE_HEAD~1, MERGE_HEAD^{tree}, MERGE_HEAD@{0}, MERGE_HEAD:dir), so a file or
# branch name that only starts with one (auto_merge.py, merge_head.txt, auto_merge-fix) is not a match.
# Round 43 (qanorm42 N2): also followed by ..., the merge-base form A...B (either side may be left out,
# meaning HEAD; by git-checkout(1), inferred and not witnessed), which round 41's prefix match refused and
# round 42's dropped (git checkout MERGE_HEAD...HEAD -- f, git restore --source=MERGE_HEAD... f). The
# ref on the right of ... is not matched (see RESIDUAL).
_GIT_OPERATION_REF = re.compile(
    r"(?:(?:main-worktree|worktrees/[^/]+)/)?"
    r"(?:MERGE_HEAD|CHERRY_PICK_HEAD|REVERT_HEAD|REBASE_HEAD|AUTO_MERGE|FETCH_HEAD)(?=\Z|[~^@:]|\.\.\.)",
    re.IGNORECASE)
# Round 15: perl options. -e and -E take the program; -0 and -l take optional digits and then read on;
# the others in PERL_REST_VALUE take the rest of the word as their value; PERL_FLAGS take none.
PERL_FLAGS = "acnpsStTuUvwWXh"
PERL_REST_VALUE = "CdDiIFmMVx"
# Round 15: cargo options before the subcommand that take the next word as their value, and ones that
# take none. Another word that starts with - may take a value, so the subcommand is unknown after it.
CARGO_VALUE_OPTIONS = frozenset(("--color", "-C", "--config", "-Z"))
CARGO_PLAIN_OPTIONS = frozenset(("-v", "-vv", "--verbose", "-q", "--quiet", "--locked", "--offline",
                                 "--frozen"))

_REMOVAL_TEXT = re.compile(
    r"(?<![A-Za-z0-9_])(?:rm|rmdir|unlink|shred|srm|wipe|delete|remove|removedirs|rmtree)(?![A-Za-z0-9_])")
_ENV_VAR_REF = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}")
_PYTHON_NAME = re.compile(r"(?:(?:python|ipython|pypy)(?:[23](?:\.[0-9]+)?[td]?)?(?:-dbg)?|py)\Z")
_ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\[[^\]]*\])?\+?=")
_FD_VAR_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}\Z")
_FD_ATTACHED_EXEC = re.compile(r"--exec(?:-batch)?=|-[A-Za-z0-9]*?[xX]")
_FIND_NEWER_XY = re.compile(r"-newer[aBcm][aBcmt]\Z")
# Constructs the lexer cannot read exactly; with a removal word in the raw text they deny as cannot-parse.
_CONTINUATION_IN_WORD = re.compile(r"(?<![ \t])\\\n")  # joins two words or a here-document line
_HEREDOC_OP = re.compile(r"<<(?!<)")
# Round 32: a here-document delimiter written as a plain name, bare or in single quotes, and the construct
# a here-document body with a removal command in command position adds (it denies with or without a
# removal word in the text, since a round 15 removal form such as git clean holds none)
_PLAIN_DELIMITER = re.compile(r"(?:'[A-Za-z_][A-Za-z0-9_]*'|[A-Za-z_][A-Za-z0-9_]*)\Z")
_HEREDOC_REMOVAL = "a removal command in command position in a here-document"
_SUBSCRIPT_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\[")
_EVAL_LIKE = frozenset(("alias", "hash", "mapfile", "readarray"))
# Round 4: with a removal word in the raw text, these deny as cannot-parse too (see FAIL-SAFE).
_BRACE_COMMAND_SUB = re.compile(r"\$\{[ \t\n|]")  # bash 5.3 ${ cmd; } and ${| cmd; }
_DOLLAR_QUOTE = re.compile(r"\$['\"]")
_HASH_ALIAS_ARRAYS = re.compile(r"(?<![A-Za-z0-9_])BASH_(?:CMDS|ALIASES)(?![A-Za-z0-9_])")
_ENV_SPLIT_OPTION = re.compile(r"-[A-Za-z0-9]*S|--sp")  # -S, a cluster ending in S, --split-string
_STRING_EVAL = frozenset(("eval", "trap", "let", "bind", "complete", "compgen", "fc", "enable"))
# Round 15: a python -c program that runs a shell command, and the perl removal calls it denies.
_PY_SHELL_CALL = re.compile(r"(?<![A-Za-z0-9_])(?:subprocess|system|popen)(?![A-Za-z0-9_])")
_PERL_NAME = re.compile(r"perl(?:5(?:\.[0-9]+)*)?\Z")
_PERL_REMOVAL = re.compile(r"(?<![A-Za-z0-9_])(?:unlink|rmtree)(?![A-Za-z0-9_])")
# Round 16 (qanorm15 M2): a perl program that runs a shell command, and the words of a text from which
# _removal_form_in reads the round 15 removal forms (git clean and the like).
_PERL_SHELL_CALL = re.compile(r"(?<![A-Za-z0-9_])(?:system|exec|qx|readpipe)(?![A-Za-z0-9_])|`")
_FORM_TOKEN = re.compile(r"-{0,2}[A-Za-z0-9_][A-Za-z0-9_-]*")

_OPERATORS = (";;&", "&>>", "<<<", "<<-", "&&", "||", "|&", ";;", ";&", ">>", ">|", "<>", "<&", ">&",
              "&>", "<<", "<", ">", "|", "&", ";", "(", ")")
_METACHARS = frozenset(" \t\n<>|&;()")
_REDIRECT_OPS = frozenset(("<", ">", ">>", ">|", "<>", "<&", ">&", "&>", "&>>", "<<", "<<-", "<<<"))
_SEPARATOR_OPS = frozenset((";", "&", "&&", "||", "|", "|&"))
_CASE_END_OPS = frozenset((";;", ";&", ";;&"))
_ANSI_SIMPLE = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n", "r": "\r",
                "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"', "?": "?"}


class ParseError(Exception):
    """The command text is outside the grammar this lexer models."""


class Word(object):
    """One shell word: text after quote removal (expansions kept as raw placeholders), the raw source,
    whether any part was quoted, and whether any part is an expansion whose value is unknown here. Round
    32: span is the (start, end) offset of the raw source in the text the lexer read, when it knows it."""

    __slots__ = ("text", "raw", "quoted", "opaque", "span")

    def __init__(self, text, raw, quoted=False, opaque=False):
        self.text = text
        self.raw = raw
        self.quoted = quoted
        self.opaque = opaque
        self.span = None

    @classmethod
    def literal(cls, text):
        return cls(text, text, False, False)


class _Ctx(object):
    """Collects the token list of every nested command body found while lexing, the constructs met
    that the lexer cannot read exactly and (round 32) each here-document body it read."""

    __slots__ = ("subs", "unreadable", "heredocs")

    def __init__(self):
        self.subs = []
        self.unreadable = set()
        # round 32: (token list, index of the operator in it, text read, body start, body end, plain
        # delimiter) per here-document
        self.heredocs = []


# --- lexer -------------------------------------------------------------------------------------------

def _match_operator(text, i):
    for op in _OPERATORS:
        if text.startswith(op, i):
            return op
    raise ParseError("no operator at offset {}".format(i))


def _lex(ctx, text, i, close, nested=False):
    """Tokenize text from i. With close, stop after the ')' that closes a $( or <( body; nested marks a
    backquote body, which ends with the text."""
    tokens = []
    pending = []
    depth = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == " " or c == "\t":
            i += 1
            continue
        if c == "\\" and text.startswith("\n", i + 1):
            i += 2
            continue
        if c == "\n":
            tokens.append(("nl", None))
            i += 1
            if pending:
                i = _read_heredocs(ctx, text, i, pending)
                pending = []
            continue
        if c == "#":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "<>" and text.startswith("(", i + 1):
            start = i
            sub, i = _lex(ctx, text, i + 2, True)
            ctx.subs.append(sub)
            # Round 18 (qanorm17 M2): the raw source is kept, so a program read from this file can be
            # tested for a removal word
            word = Word("<(...)", text[start:i], False, True)
            if i < n and text[i] not in _METACHARS:
                # bash keeps reading the same word after a process substitution, so a # (or any
                # other character) glued to its ) belongs to that word and starts no comment
                rest, i = _read_word(ctx, text, i)
                word = Word(word.text + rest.text, word.raw + rest.raw, rest.quoted, True)
            tokens.append(("w", word))
            continue
        if c == "(" and text.startswith("((", i):
            # An arithmetic command (( ... )), also the for (( ... )) header: its << and <<= are shifts,
            # not here-documents. If it does not close with )), read it as nested subshells, as bash does.
            mark = len(ctx.subs)
            try:
                end = _scan_arith(ctx, text, i + 2)
            except ParseError:
                del ctx.subs[mark:]
            else:
                tokens.append(("w", Word("((...))", text[i:end], False, True)))
                i = end
                continue
        if c in _METACHARS:
            op = _match_operator(text, i)
            i += len(op)
            if op == "(":
                depth += 1
            elif op == ")":
                if close and depth == 0:
                    if pending:
                        # Round 10: bash reads this here-document's body from the lines after the
                        # substitution closes, which this lexer does not model
                        raise ParseError("here-document opened in a substitution that closes first")
                    return tokens, i
                depth -= 1
            tokens.append(("op", op))
            if op == "<<<" or (op in ("<<", "<<-") and not _RULES["here-document narrowing"]):
                # Round 11 (qanorm10 F1): here-document tracking fell out of step with bash in rounds 8
                # to 10 and again here, so with a removal word anywhere in the raw text a here-string
                # denies as cannot-parse. Round 32 (D-2384): a here-document denies that way only when a
                # body holds a removal command in command position (see _read_heredocs and FAIL-SAFE)
                ctx.unreadable.add("a here-document or here-string")
            if op in ("<<", "<<-"):
                op_index = len(tokens) - 1
                while i < n and text[i] in " \t":
                    i += 1
                if i >= n or text[i] in _METACHARS:
                    raise ParseError("here-document operator without a delimiter")
                start = i
                word, i = _read_word(ctx, text, i)
                word.span = (start, i)
                if any(s in word.raw for s in ("$(", "${", "$[", "`")):
                    # bash matches such a delimiter as written, not as this lexer's placeholder text
                    raise ParseError("here-document delimiter with an expansion")
                tokens.append(("w", word))
                pending.append((word.text, op == "<<-", word.quoted, tokens, op_index,
                                bool(_PLAIN_DELIMITER.match(word.raw))))
            continue
        start = i
        word, i = _read_word(ctx, text, i)
        word.span = (start, i)
        if (i < n and text[i] in "<>" and not word.quoted
                and (word.raw.isdigit() or _FD_VAR_RE.match(word.raw))):
            continue  # a file-descriptor prefix of the redirection operator that follows
        tokens.append(("w", word))
    if close:
        raise ParseError("unterminated command or process substitution")
    if nested and pending:
        raise ParseError("here-document opened in a backquote body that closes first")
    return tokens, i


def _read_word(ctx, text, i):
    n = len(text)
    start = i
    parts = []
    quoted = False
    opaque = False
    paren = 0
    array = False
    braces = []  # per unquoted { not yet closed: whether a , or .. has followed it (brace expansion)
    while i < n:
        c = text[i]
        if c in _METACHARS:
            if paren and c in "<>" and text.startswith("(", i + 1):
                # Round 18 (qanorm17 M1): bash runs a process substitution inside an array assignment
                # NAME=( ... <(cmd) ... ), so lex its body as a command
                sub, i = _lex(ctx, text, i + 2, True)
                ctx.subs.append(sub)
                parts.append("<(...)")
                opaque = True
                continue
            if paren:
                if c == "(":
                    paren += 1
                elif c == ")":
                    paren -= 1
                parts.append(c)
                i += 1
                continue
            if c == "(" and _ASSIGN_RE.fullmatch(text, start, i):
                paren = 1  # an array assignment NAME=( ... )
                array = True
                parts.append(c)
                i += 1
                continue
            break
        if c == "\\":
            if i + 1 >= n:
                parts.append("\\")
                i += 1
            elif text[i + 1] == "\n":
                i += 2
            else:
                parts.append(text[i + 1])
                quoted = True
                i += 2
            continue
        if c == "'":
            j = text.find("'", i + 1)
            if j < 0:
                raise ParseError("unterminated single quote")
            parts.append(text[i + 1:j])
            quoted = True
            i = j + 1
            continue
        if c == '"':
            i, sub_opaque = _read_double(ctx, text, i + 1, parts)
            quoted = True
            opaque = opaque or sub_opaque
            continue
        if c == "$":
            i, sub_opaque, sub_quoted = _read_dollar(ctx, text, i, parts, False)
            opaque = opaque or sub_opaque
            quoted = quoted or sub_quoted
            continue
        if c == "`":
            i = _read_backtick(ctx, text, i + 1)
            parts.append("`...`")
            opaque = True
            continue
        if c in "*?[":
            opaque = True
        if c == "{":
            braces.append(False)
        elif braces and (c == "," or (c == "." and text.startswith(".", i + 1))):
            braces[-1] = True
        elif c == "}" and braces and braces.pop():
            opaque = True  # an unquoted { with a , or .. before its closing }: a brace expansion
        parts.append(c)
        i += 1
    if paren:
        raise ParseError("unterminated array assignment")
    if array and "#" in text[start:i]:
        # paren mode counts a ( or ) inside a comment of an array assignment, which bash ignores
        ctx.unreadable.add("a # inside an array assignment")
    return Word("".join(parts), text[start:i], quoted, opaque), i


def _read_double(ctx, text, i, parts):
    n = len(text)
    opaque = False
    while i < n:
        c = text[i]
        if c == '"':
            return i + 1, opaque
        if c == "\\" and i + 1 < n:
            nx = text[i + 1]
            if nx in '$`"\\':
                parts.append(nx)
                i += 2
            elif nx == "\n":
                i += 2
            else:
                parts.append("\\")
                i += 1
            continue
        if c == "$":
            i, sub_opaque, _quoted = _read_dollar(ctx, text, i, parts, True)
            opaque = opaque or sub_opaque
            continue
        if c == "`":
            i = _read_backtick(ctx, text, i + 1, True)
            parts.append("`...`")
            opaque = True
            continue
        parts.append(c)
        i += 1
    raise ParseError("unterminated double quote")


def _read_dollar(ctx, text, i, parts, in_dq):
    """Read a $-construct at text[i]; return (next index, opaque, quoted)."""
    n = len(text)
    nx = text[i + 1] if i + 1 < n else ""
    if nx == "'" and not in_dq:
        decoded, i = _ansi_c(text, i + 2)
        parts.append(decoded)
        return i, False, True
    if nx == '"' and not in_dq:
        return i + 1, False, False
    if nx == "(":
        if text.startswith("((", i + 1):
            i = _scan_arith(ctx, text, i + 3)
        else:
            sub, i = _lex(ctx, text, i + 2, True)
            ctx.subs.append(sub)
        parts.append("$(...)")
        return i, True, False
    if nx == "[":
        i = _scan_bracket_arith(ctx, text, i + 2)
        parts.append("$[...]")
        return i, True, False
    if nx == "{":
        i = _scan_brace(ctx, text, i + 2)
        parts.append("${...}")
        return i, True, False
    if nx and nx.isdigit():
        parts.append(text[i:i + 2])
        return i + 2, True, False
    if nx and (nx.isalpha() or nx == "_"):
        j = i + 1
        while j < n and (text[j].isalnum() or text[j] == "_"):
            j += 1
        parts.append(text[i:j])
        return j, True, False
    if nx and nx in "@*#?$!-":
        parts.append(text[i:i + 2])
        return i + 2, True, False
    parts.append("$")
    return i + 1, False, False


def _ansi_c(text, i, keep_nul=False):
    """Decode a $'...' body from i; bash cuts the decoded string at its first NUL unless keep_nul."""
    n = len(text)
    out = []
    while i < n:
        c = text[i]
        if c == "'":
            decoded = "".join(out)
            return (decoded if keep_nul else decoded.split("\x00", 1)[0]), i + 1
        if c == "\\" and i + 1 < n:
            nx = text[i + 1]
            if nx in _ANSI_SIMPLE:
                out.append(_ANSI_SIMPLE[nx])
                i += 2
            elif nx in "01234567":
                j = i + 1
                while j < n and j < i + 4 and text[j] in "01234567":
                    j += 1
                out.append(_chr(int(text[i + 1:j], 8)))
                i = j
            elif nx in "xuU":
                width = {"x": 2, "u": 4, "U": 8}[nx]
                j = i + 2
                while j < n and j < i + 2 + width and text[j] in "0123456789abcdefABCDEF":
                    j += 1
                if j == i + 2:
                    out.append("\\" + nx)
                else:
                    out.append(_chr(int(text[i + 2:j], 16)))
                i = j
            elif nx == "c" and i + 2 < n:
                out.append(_chr(ord(text[i + 2]) & 0x1F))
                i += 3
            else:
                out.append("\\" + nx)
                i += 2
            continue
        out.append(c)
        i += 1
    raise ParseError("unterminated $'...' string")


def _chr(code):
    try:
        return chr(code)
    except (ValueError, OverflowError):
        raise ParseError("escape outside the Unicode range")


def _scan_arith(ctx, text, i):
    n = len(text)
    depth = 0
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "$" and text.startswith("(", i + 1) and not text.startswith("((", i + 1):
            sub, i = _lex(ctx, text, i + 2, True)
            ctx.subs.append(sub)
            continue
        if c == "$" and text.startswith("{", i + 1):
            i = _scan_brace(ctx, text, i + 2)
            continue
        if c == "`":
            i = _read_backtick(ctx, text, i + 1)
            continue
        if c in "'\"":
            # bash honours quotes when it finds the closing )); this scanner does not
            ctx.unreadable.add("a quote inside arithmetic")
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                if text.startswith(")", i + 1):
                    return i + 2
                raise ParseError("arithmetic expansion not closed by ))")
            depth -= 1
        i += 1
    raise ParseError("unterminated arithmetic expansion")


def _scan_bracket_arith(ctx, text, i):
    """The old arithmetic expansion $[ ... ]: like $(( ... )), its << is a shift."""
    n = len(text)
    depth = 0
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "$" and text.startswith("(", i + 1) and not text.startswith("((", i + 1):
            sub, i = _lex(ctx, text, i + 2, True)
            ctx.subs.append(sub)
            continue
        if c == "$" and text.startswith("{", i + 1):
            i = _scan_brace(ctx, text, i + 2)
            continue
        if c == "`":
            i = _read_backtick(ctx, text, i + 1)
            continue
        if c in "'\"":
            # bash honours quotes when it finds the closing ]; this scanner does not
            ctx.unreadable.add("a quote inside arithmetic")
        if c == "[":
            depth += 1
        elif c == "]":
            if depth == 0:
                return i + 1
            depth -= 1
        i += 1
    raise ParseError("unterminated $[ ... ] arithmetic expansion")


def _scan_brace(ctx, text, i):
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "}":
            return i + 1
        if c == "'":
            j = text.find("'", i + 1)
            if j < 0:
                raise ParseError("unterminated single quote in ${...}")
            i = j + 1
            continue
        if c == '"':
            i, _opaque = _read_double(ctx, text, i + 1, [])
            continue
        if c == "$":
            i, _opaque, _quoted = _read_dollar(ctx, text, i, [], False)
            continue
        if c == "`":
            i = _read_backtick(ctx, text, i + 1)
            continue
        i += 1
    raise ParseError("unterminated ${...}")


def _read_backtick(ctx, text, i, in_dq=False):
    n = len(text)
    body = []
    while i < n:
        c = text[i]
        if c == "`":
            sub, _end = _lex(ctx, "".join(body), 0, False, True)
            ctx.subs.append(sub)
            return i + 1
        if c == "\\" and i + 1 < n and text[i + 1] in "`\\$":
            body.append(text[i + 1])
            i += 2
            continue
        if in_dq and c == "\\" and text.startswith('"', i + 1):
            # Round 14 (qanorm13 F1): in double quotes bash also reads this \" as ", which this lexer
            # does not model, so the body may hide a command (see FAIL-SAFE)
            ctx.unreadable.add('a backquote inside double quotes holding \\"')
        body.append(c)
        i += 1
    raise ParseError("unterminated backquote")


def _read_heredocs(ctx, text, i, pending):
    n = len(text)
    for delim, strip_tabs, quoted, tokens, op_index, plain in pending:
        body = []
        found = False
        body_start = i
        body_end = i
        while i < n:
            j = text.find("\n", i)
            end = n if j < 0 else j
            line = text[i:end]
            body_end = i
            i = n if j < 0 else j + 1
            if (line.lstrip("\t") if strip_tabs else line) == delim:
                found = True
                break
            body.append(line)
        if not found:
            raise ParseError("here-document not closed by its delimiter line")
        body_text = "\n".join(body)
        ctx.heredocs.append((tokens, op_index, text, body_start, body_end,
                             plain and (quoted or not any(c in body_text for c in "$`\\"))))
        # Round 32 (D-2384): a body line that holds a removal command in command position denies as
        # cannot-parse (the tracking may have hidden a line that bash runs); other body text is data
        if _RULES["here-document command position"] and (
                _body_runs_removal(body_text)
                or (_RULES["here-document command words"] and _body_command_words_run_removal(body_text))):
            ctx.unreadable.add(_HEREDOC_REMOVAL)
        if not quoted:
            _scan_expanding(ctx, "\n".join(body))
    return i


def _scan_expanding(ctx, s):
    """An unquoted here-document body: plain text, except that $( ), ${ } and backquotes execute."""
    n = len(s)
    i = 0
    while i < n:
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "$" and i + 1 < n and s[i + 1] in "({":
            i, _opaque, _quoted = _read_dollar(ctx, s, i, [], True)
            continue
        if c == "`":
            i = _read_backtick(ctx, s, i + 1)
            continue
        i += 1


# --- command positions -------------------------------------------------------------------------------

def _is_assignment(raw):
    """A NAME=, NAME+= or NAME[...]= word; bash joins a line continuation inside it first."""
    return bool(_ASSIGN_RE.match(raw.replace("\\\n", "")))


class _Argv(list):
    """Round 21 (qanorm20 F1): an argv that also keeps the NAME=VALUE words written before it, which the
    command reads as its environment (an awk program reads them through ENVIRON)."""
    __slots__ = ("assigns",)

    def __init__(self, words, assigns):
        list.__init__(self, words)
        self.assigns = list(assigns)


def _command_argvs(tokens):
    """Return the argv (list of Word) of every simple command in one token list, in order."""
    argvs = []
    state = {"argv": [], "assigned": False, "time": False, "after": False, "redirected": False, "assigns": []}
    stack = []
    mode = "normal"
    target = False
    hdr_depth = 0
    hdr_words = 0
    pattern_words = 0
    n = len(tokens)
    k = 0

    def finish():
        if state["argv"]:
            argvs.append(_Argv(state["argv"], state["assigns"]))
        state["argv"] = []
        state["assigns"] = []
        state["assigned"] = False
        state["time"] = False
        state["after"] = False
        state["redirected"] = False

    def close(kind):
        if not stack or stack[-1] != kind:
            raise ParseError("unbalanced compound command")
        stack.pop()
        state["after"] = True

    def require(kind):
        if not stack or stack[-1] != kind:
            raise ParseError("reserved word out of place")

    while k < n:
        kind, val = tokens[k]
        k += 1
        if target:
            if kind != "w":
                raise ParseError("redirection without a target")
            target = False
            continue
        if mode == "for":
            if kind == "op":
                if val == "(":
                    hdr_depth += 1
                elif val == ")":
                    hdr_depth -= 1
                    if hdr_depth < 0:
                        raise ParseError("unbalanced for header")
                elif hdr_depth == 0 and val == ";":
                    mode = "normal"
                elif hdr_depth == 0 and val not in _REDIRECT_OPS:
                    raise ParseError("unexpected operator in a for header")
                continue
            if kind == "nl":
                if hdr_depth == 0:
                    mode = "normal"
                continue
            hdr_words += 1
            if hdr_depth == 0 and val.raw == "do" and hdr_words == 2:
                mode = "normal"
            continue
        if mode == "case-word":
            if kind == "nl":
                continue
            if kind != "w":
                raise ParseError("case without a word")
            mode = "case-in"
            continue
        if mode == "case-in":
            if kind == "nl":
                continue
            if kind == "w" and val.raw == "in":
                mode = "case-pattern"
                pattern_words = 0
                continue
            raise ParseError("case without in")
        if mode == "case-pattern":
            if kind == "nl":
                continue
            if kind == "w":
                if val.raw == "esac" and pattern_words == 0:
                    close("case")
                    mode = "normal"
                    continue
                pattern_words += 1
                continue
            if val == "(" and pattern_words == 0:
                continue
            if val == "|":
                continue
            if val == ")" and pattern_words:
                mode = "normal"
                continue
            raise ParseError("malformed case pattern")
        if mode == "dbl":
            if kind == "w" and val.raw == "]]":
                mode = "normal"
                state["after"] = True
            continue
        # normal mode
        if kind == "nl" or (kind == "op" and val in _SEPARATOR_OPS):
            finish()
            continue
        if kind == "op":
            if val in _CASE_END_OPS:
                finish()
                require("case")
                mode = "case-pattern"
                pattern_words = 0
                continue
            if val in _REDIRECT_OPS:
                target = True
                state["redirected"] = True  # bash reads no reserved word after a redirection
                continue
            if val == "(":
                argv = state["argv"]
                if not argv and not state["assigned"] and not state["after"]:
                    stack.append("(")
                    continue
                if len(argv) == 1 and k < n and tokens[k] == ("op", ")"):
                    k += 1  # NAME () compound-command: a function definition
                    # Round 13 (qanorm12 finding 2): the NAME is defined, not run, as for function NAME
                    state["argv"] = []
                    finish()
                    continue
                raise ParseError("unexpected (")
            if val == ")":
                finish()
                close("(")
                continue
            raise ParseError("unexpected operator {}".format(val))
        # a word
        if state["after"]:
            raise ParseError("word after a compound command")
        if state["argv"]:
            state["argv"].append(val)
            continue
        raw = val.raw
        if not state["assigned"] and not state["redirected"]:
            if raw == "if":
                stack.append("if")
                continue
            if raw in ("while", "until"):
                stack.append("loop")
                continue
            if raw in ("then", "elif", "else"):
                require("if")
                continue
            if raw == "do":
                require("loop")
                continue
            if raw in ("!", "coproc"):
                continue
            if raw == "{":
                stack.append("{")
                continue
            if raw == "fi":
                close("if")
                continue
            if raw == "done":
                close("loop")
                continue
            if raw == "}":
                close("{")
                continue
            if raw == "esac":
                close("case")
                continue
            if raw in ("for", "select"):
                stack.append("loop")
                mode = "for"
                hdr_depth = 0
                hdr_words = 0
                continue
            if raw == "case":
                stack.append("case")
                mode = "case-word"
                continue
            if raw == "[[":
                mode = "dbl"
                continue
            if raw == "function":
                if k >= n or tokens[k][0] != "w":
                    raise ParseError("function without a name")
                k += 1
                if k + 1 < n and tokens[k] == ("op", "(") and tokens[k + 1] == ("op", ")"):
                    k += 2
                continue
            if raw == "time":
                state["time"] = True
                continue
            if state["time"] and raw.startswith("-"):
                if raw != "-p":
                    raise ParseError("a time option other than -p")  # bash reads it as the command word
                continue
        if _is_assignment(raw):
            state["assigned"] = True
            state["assigns"].append(val)
            continue
        state["argv"].append(val)
    finish()
    if stack or mode != "normal" or target:
        raise ParseError("incomplete command")
    return argvs


# --- argv checks -------------------------------------------------------------------------------------

class _Spec(object):
    __slots__ = ("flags", "args", "optargs", "long_args", "long_flags", "numeric", "split", "dash",
                 "long_optargs")

    def __init__(self, flags="", args="", optargs="", long_args=(), long_flags=(), numeric=False,
                 split=None, dash=False, long_optargs=()):
        self.flags = flags
        self.args = args
        self.optargs = optargs
        self.long_args = frozenset(long_args)
        self.long_flags = frozenset(long_flags) | frozenset(("--help", "--version"))
        self.numeric = numeric
        self.split = split
        self.dash = dash
        # Round 42 (qanorm41 F1): long options whose value is optional (PATH_APPENDERS). Round 43 (qanorm42
        # N6): round 42's placement field, which nothing read, is gone
        self.long_optargs = frozenset(long_optargs)


WRAPPERS = {
    "command": _Spec(flags="pvV"),
    "exec": _Spec(flags="cl", args="a"),
    "env": _Spec(flags="i0v", args="uCS", split="S", dash=True,
                 long_args=("--unset", "--chdir", "--split-string"),
                 long_flags=("--ignore-environment", "--null", "--debug", "--default-signal",
                             "--ignore-signal", "--block-signal", "--list-signal-handling")),
    "sudo": _Spec(flags="AbEHiKkLlnPSsVBN", args="CDghpRrtTUu",
                  long_args=("--chdir", "--close-from", "--group", "--host", "--prompt", "--role",
                             "--type", "--command-timeout", "--other-user", "--user", "--chroot"),
                  long_flags=("--askpass", "--background", "--bell", "--edit", "--preserve-env",
                              "--set-home", "--login", "--remove-timestamp", "--reset-timestamp", "--list",
                              "--non-interactive", "--preserve-groups", "--stdin", "--shell", "--validate")),
    "doas": _Spec(flags="nsL", args="uC"),
    "nohup": _Spec(),
    "nice": _Spec(args="n", numeric=True, long_args=("--adjustment",)),
    "ionice": _Spec(flags="t", args="cnpPu",
                    long_args=("--class", "--classdata", "--pid", "--pgid", "--uid"),
                    long_flags=("--ignore",)),
    "timeout": _Spec(flags="v", args="sk", long_args=("--signal", "--kill-after"),
                     long_flags=("--preserve-status", "--foreground", "--verbose")),
    "time": _Spec(flags="apqvV", args="fo", long_args=("--format", "--output"),
                  long_flags=("--append", "--portability", "--quiet", "--verbose")),
    "stdbuf": _Spec(args="ioe", long_args=("--input", "--output", "--error")),
    "builtin": _Spec(),
    "busybox": _Spec(),
    "xargs": _Spec(flags="0prtxo", args="adEILnPs", optargs="eil",
                   long_args=("--arg-file", "--delimiter", "--max-args", "--max-procs", "--max-chars",
                              "--process-slot-var"),
                   long_flags=("--null", "--interactive", "--no-run-if-empty", "--verbose", "--exit",
                               "--open-tty", "--show-limits", "--eof", "--replace", "--max-lines")),
    # Round 15: setsid, flock (FILE COMMAND, or FILE -c STRING) and taskset (MASK COMMAND)
    "setsid": _Spec(flags="cfwhV", long_flags=("--ctty", "--fork", "--wait")),
    "flock": _Spec(flags="sexnouFhV", args="wE", long_args=("--wait", "--timeout", "--conflict-exit-code"),
                   long_flags=("--shared", "--exclusive", "--unlock", "--nonblock", "--nb", "--nonblocking",
                               "--close", "--no-fork", "--verbose")),
    "taskset": _Spec(flags="apchV", long_flags=("--all-tasks", "--pid", "--cpu-list")),
    # Round 16 (qanorm15 B1): chrt ([PRIORITY] COMMAND; chrt -p and -m run nothing), unshare, fakeroot,
    # eatmydata, strace and ltrace
    "chrt": _Spec(flags="abdfiorRmpvhV", args="TPD",
                  long_args=("--sched-runtime", "--sched-period", "--sched-deadline"),
                  long_flags=("--all-tasks", "--batch", "--deadline", "--fifo", "--idle", "--other", "--rr",
                              "--reset-on-fork", "--max", "--pid", "--verbose")),
    "unshare": _Spec(flags="muinpUCTfrchV", args="RwSG",
                     long_args=("--propagation", "--setgroups", "--root", "--wd", "--setuid", "--setgid",
                                "--monotonic", "--boottime", "--map-user", "--map-group", "--map-users",
                                "--map-groups"),
                     long_flags=("--mount", "--uts", "--ipc", "--net", "--pid", "--user", "--cgroup",
                                 "--time", "--fork", "--map-root-user", "--map-current-user", "--kill-child",
                                 "--mount-proc", "--keep-caps", "--map-auto")),
    "fakeroot": _Spec(flags="uhv", args="lisb", long_args=("--lib", "--faked", "--fd-base"),
                      long_flags=("--unknown-is-real",)),
    "eatmydata": _Spec(),
    "strace": _Spec(flags="AcCdDfFhiknqrtTvVwxyYzZ", args="abeEIoOpPsSuUX",
                    long_args=("--output", "--trace", "--signal", "--string-limit", "--user", "--env",
                               "--attach", "--trace-path"),
                    long_flags=("--follow-forks", "--output-separately", "--summary-only", "--summary",
                                "--seccomp-bpf")),
    "ltrace": _Spec(flags="bcCfghiLrStTV", args="aADeFlnopsuwx",
                    long_args=("--align", "--config", "--indent", "--library", "--output"),
                    long_flags=("--demangle", "--no-signals")),
}
# Round 41 (qanorm40 N8): gxargs, GNU xargs as installed beside a BSD xargs (macOS, the BSDs), is read as
# xargs is, at every place the guard names xargs (_XARGS_NAMES)
WRAPPERS["gxargs"] = WRAPPERS["xargs"]
_XARGS_NAMES = frozenset(("xargs", "gxargs"))
# Round 16 (qanorm15 B1): pipx run and poetry run ([OPTIONS] run [OPTIONS] COMMAND), checked as uv run is.
# pipx run runs the PyPI app named COMMAND, which the guard checks as a command word (the safe direction).
RUNNERS = {
    "pipx": _Spec(flags="qveh", args="i",
                  long_args=("--spec", "--python", "--index-url", "--pip-args", "--backend"),
                  long_flags=("--path", "--pypackages", "--no-cache", "--fetch-missing-python",
                              "--system-site-packages", "--editable", "--verbose", "--quiet", "--global")),
    "poetry": _Spec(flags="qvVhn", args="CP", long_args=("--directory", "--project"),
                    long_flags=("--quiet", "--verbose", "--no-interaction", "--ansi", "--no-ansi",
                                "--no-plugins", "--no-cache")),
}
# Round 15: uv options, before run and after it. An option it does not know denies as cannot-parse when a
# removal word follows, as for the wrappers above.
_UV_SPEC = _Spec(flags="qvnUhVms", args="pCPfi",
                 long_args=("--with", "--with-editable", "--with-requirements", "--python", "--project",
                            "--directory", "--env-file", "--extra", "--group", "--only-group", "--no-group",
                            "--package", "--index", "--default-index", "--index-url", "--extra-index-url",
                            "--find-links", "--index-strategy", "--keyring-provider", "--resolution",
                            "--prerelease", "--exclude-newer", "--link-mode", "--config-setting",
                            "--config-file", "--cache-dir", "--color", "--upgrade-package",
                            "--reinstall-package", "--refresh-package", "--python-platform",
                            "--allow-insecure-host"),
                 long_flags=("--no-sync", "--frozen", "--locked", "--isolated", "--no-project", "--no-dev",
                             "--dev", "--all-extras", "--all-groups", "--no-default-groups", "--module",
                             "--script", "--gui-script", "--active", "--no-active", "--no-editable",
                             "--exact", "--upgrade", "--reinstall", "--refresh", "--offline", "--no-cache", "--quiet",
                             "--verbose", "--native-tls", "--no-progress", "--no-config",
                             "--no-python-downloads", "--compile-bytecode", "--no-build-isolation",
                             "--no-build", "--no-binary", "--no-sources", "--no-env-file", "--all-packages"))


def _basename(text):
    return text.rsplit("/", 1)[-1]


def _uncertain_scan(words):
    """An argv the guard cannot read past: deny (cannot parse) when any word holds a removal word, in its
    text or in its raw source (the text of a substitution is a placeholder: sudo $(which rm) -rf y)."""
    for word in words:
        if _REMOVAL_TEXT.search(word.text) or _REMOVAL_TEXT.search(word.raw):
            return CANNOT_PARSE
    return None


def _check_argv(words, depth, assigns=()):
    """assigns: the NAME=VALUE words before this argv, also those a wrapper passed on (env, sudo), which
    an awk program reads through ENVIRON (round 21)."""
    if depth > MAX_CHECK_DEPTH:
        # Round 17 (qanorm16 F5): past the cap, a round 15 removal form denies as a removal word does;
        # round 18 (qanorm17 m6): the word getattr, NFKC folding and the decoding of _has_removal_text count
        if any(_has_removal_text(w.text) or _has_removal_text(w.raw) for w in words):
            return CANNOT_PARSE
        return _uncertain_scan(words) or _form_scan(words)
    j = 0
    while j < len(words) and _is_assignment(words[j].raw):
        j += 1
    if j >= len(words):
        return None
    word = words[j]
    if word.opaque:
        # a command word built at run time: residual, unless a removal word is in that argv
        return CANNOT_PARSE if _REMOVAL_TEXT.search(word.raw) else _uncertain_scan(words[j:])
    name = _basename(word.text)
    rest = words[j + 1:]
    assigns = list(assigns) + list(words[:j])
    if name in REMOVERS:
        if len(rest) == 1 and rest[0].text in ("--help", "--version"):
            return None  # it only prints
        return DENY
    if name in _FIND_NAMES:
        return _check_find(rest, depth, name == "bfs")
    if name in ("fd", "fdfind"):
        return _check_fd(rest, depth)
    if name == "gio":
        return DENY if rest and rest[0].text == "remove" else None
    if name == "git":
        return _check_git(rest, depth)
    if name == "trap":
        return _check_trap(rest, depth)
    if name == "eval":
        return _check_eval(rest, depth)
    if _PYTHON_NAME.match(name):
        return _check_python(rest, depth, name.startswith("ipython"))
    if name == "fish":
        return _check_fish(rest, depth)
    if name in SHELL_NAMES:
        return _check_shell(rest, depth)
    if _PERL_NAME.match(name):
        return _check_perl(rest, depth)
    if name == "rsync":
        return _check_rsync(rest)
    if name == "cargo":
        return _check_cargo(rest)
    if name == "uv":
        return _check_uv(rest, depth)
    if name in RUNNERS:
        return _check_runner(RUNNERS[name], rest, depth)
    if name == "su":
        return _check_su(rest, depth)
    if name == "jobs":
        return _check_jobs(rest, depth)
    # Round 20 (qanorm19 MINOR-1): ssh with a remote command, awk system() and sed e run a command; each
    # still has the unknown-command scan (it may run a later word)
    if name == "ssh":
        return _check_ssh(rest, depth) or _unknown_command_scan(rest, depth)
    if name in _AWK_NAMES:
        return _check_awk(rest, assigns) or _unknown_command_scan(rest, depth, assigns)
    if name in ("sed", "gsed"):
        return _check_sed(rest) or _unknown_command_scan(rest, depth)
    # Round 41 (qanorm40 N1): GNU parallel, sem, xe and rush append the items they read to their command
    # as xargs does; each keeps the unknown-command scan. Round 43 (qanorm42 N1 to N3, N6): behind them,
    # and behind xargs and gxargs, a git command whose subcommand the guard reads denies as cannot-parse
    # whatever the wrapper's options; round 45 (qanorm44 F1, F2): every git command there but one whose
    # word right after git is a listed read-only subcommand (_appended_git_check, _GIT_APPENDED_ALLOWED)
    # Round 46 (qanorm45 F1, F2, F4): and first, the command they run must start with a listed plain
    # program (_appended_command_check, _APPENDED_PLAIN_PROGRAMS); xargs and gxargs with no command run echo
    if name in _PARALLEL_NAMES:
        return (_unknown_command_scan(rest, depth, assigns)
                or _appended_command_check(rest, _appended_parallel_start(name, rest), True)
                or _appended_git_check(rest))
    if name in _XARGS_NAMES:
        result = _check_wrapper(name, WRAPPERS[name], rest, depth, assigns)
        if result is not None:
            return result
        start, ok, _seen, _split = _parse_options(WRAPPERS[name], rest)
        if ok and start >= len(rest):
            return _appended_git_check(rest)
        return _appended_command_check(rest, start if ok else None) or _appended_git_check(rest)
    spec = WRAPPERS.get(name)
    if spec is not None:
        return _check_wrapper(name, spec, rest, depth, assigns)
    if name in _INERT_BUILTINS:
        return None
    # Round 16 (qanorm15 B1): a command word the guard does not know may be a wrapper that runs a later word
    return _unknown_command_scan(rest, depth, assigns)


def _unknown_command_scan(words, depth, assigns=()):
    """The argv of a command word the guard does not know: deny (cannot parse) when a later unquoted word
    is a removal command name (or a path ending in one), or git followed by a removal subcommand form,
    or (round 23) cargo or rsync followed by a form the cargo or rsync rule denies. Round 20 (qanorm19
    MINOR-1): also when the full argv check, run from a later unquoted word that names a shell, an
    interpreter, find or a wrapper it knows, finds a removal or a form it cannot read
    (chroot /srv sh -c 'rm -rf x', watch find . -delete)."""
    for idx, word in enumerate(words):
        if word.quoted or word.opaque:
            continue
        name = _basename(word.text)
        if name in REMOVERS:
            return CANNOT_PARSE
        if name == "git" and depth < MAX_CHECK_DEPTH and _check_git(words[idx + 1:], depth + 1) is not None:
            return CANNOT_PARSE
        # Round 23 (qanorm22 F1): the other round 15 removal forms, cargo clean and rsync with a deleting
        # option, start the same check as git does (chroot /srv cargo clean, mywrap rsync -a --delete a b)
        if name in ("cargo", "rsync") and depth < MAX_CHECK_DEPTH and _check_argv(
                words[idx:], depth + 1, assigns) is not None:
            return CANNOT_PARSE
        if _starts_known_argv(name):
            if depth >= MAX_CHECK_DEPTH or not _spend_scan_budget():
                # past the depth cap or the scan budget, as past the depth cap of _check_argv
                if any(_has_removal_text(w.text) or _has_removal_text(w.raw) for w in words[idx:]):
                    return CANNOT_PARSE
                return _form_scan(words[idx:])
            if _check_argv(words[idx:], depth + 1, assigns) is not None:
                return CANNOT_PARSE
    return None


# Round 20 (qanorm19 MINOR-1): the command words _check_argv has a rule for; any other may be a wrapper it
# does not know. A later word of such a command that names a shell, an interpreter, find or a wrapper it
# knows starts a full argv check. The scan budget bounds that check per command (a wrapper inside an
# unknown command inside a wrapper, and so on, would otherwise branch at each level): past it, a removal
# word or a round 15 removal form in the rest of the argv denies as cannot-parse.
_RULE_NAMES = frozenset(("find", "gfind", "bfs", "fd", "fdfind", "gio", "git", "trap", "eval", "rsync", "cargo", "uv", "su",
                         "jobs", "ssh", "sed", "gsed", "awk", "gawk", "mawk", "nawk"))
_AWK_NAMES = frozenset(("awk", "gawk", "mawk", "nawk"))
_SCAN_BUDGET = 2000
_scan_budget = [_SCAN_BUDGET]


def _spend_scan_budget():
    if _scan_budget[0] <= 0:
        return False
    _scan_budget[0] -= 1
    return True


def _has_rule(name):
    """Whether _check_argv has a rule for this command word (a removal program, a command, wrapper or
    runner it reads, or a bash builtin that never runs an operand)."""
    return (name in REMOVERS or name in _RULE_NAMES or name in SHELL_NAMES or name in WRAPPERS
            or name in RUNNERS or name in _INERT_BUILTINS or bool(_PYTHON_NAME.match(name))
            or bool(_PERL_NAME.match(name)))


def _starts_known_argv(name):
    """A later word of an unknown command that starts a full argv check: a shell, su, an interpreter
    (python, perl, awk), find or fd, ssh, eval, or a wrapper or runner it knows."""
    return (name in SHELL_NAMES or name in WRAPPERS or name in RUNNERS or name in _AWK_NAMES
            or name in _FIND_NAMES or name in ("su", "fd", "fdfind", "ssh", "sed", "gsed", "eval", "uv")
            or bool(_PYTHON_NAME.match(name)) or bool(_PERL_NAME.match(name)))


def _removal_form_in(text):
    """Whether a text names a round 15 removal form: git clean, git reset --hard, git stash -u or -a, git
    checkout or switch -f (or --discard-changes), git checkout-index -f, git submodule deinit -f, git
    read-tree -u --reset (round 19), git submodule update -f (round 30), git rebase --abort or --skip and
    git am --abort (round 31), git merge --abort and git cherry-pick --abort (round 37), git am --skip,
    git cherry-pick --skip and git revert --abort or --skip (round 38; each through
    GIT_ABANDON_OPTIONS), cargo clean, or rsync --delete or --remove-source-files. A word test
    over the whole text, in any order (the safe direction)."""
    tokens = set(_FORM_TOKEN.findall(text))
    if "git" in tokens:
        if "clean" in tokens:
            return True
        if "reset" in tokens and any(len(t) > 2 and "--hard".startswith(t) for t in tokens):
            return True
        if "stash" in tokens and any(
                (t.startswith("--") and len(t) > 2
                 and ("--include-untracked".startswith(t) or "--all".startswith(t)))
                or (t.startswith("-") and not t.startswith("--") and re.search("[ua]", t[1:]))
                for t in tokens):
            return True
        if ("checkout" in tokens or "switch" in tokens) and any(
                (t.startswith("--") and len(t) > 2
                 and ("--force".startswith(t) or "--discard-changes".startswith(t)))
                or (t.startswith("-") and not t.startswith("--") and "f" in t[1:])
                for t in tokens):
            return True
        # Round 19 (qanorm18 MEDIUM-1): the round 18 git discard forms, git checkout-index -f, git
        # submodule deinit -f and git read-tree -u --reset; round 30 (qanorm29 F1): git submodule update -f
        force = any((t.startswith("--") and len(t) > 2 and "--force".startswith(t))
                    or (t.startswith("-") and not t.startswith("--") and "f" in t[1:]) for t in tokens)
        if force and ("checkout-index" in tokens
                      or ("submodule" in tokens and ("deinit" in tokens or "update" in tokens))):
            return True
        if ("read-tree" in tokens and any(len(t) > 4 and "--reset".startswith(t) for t in tokens)
                and any(t.startswith("-") and not t.startswith("--") and "u" in t[1:] for t in tokens)):
            return True
        # Round 31 (qanorm30 MINOR-1): git rebase --abort or --skip and git am --abort; round 38: every
        # --abort and --skip in GIT_ABANDON_OPTIONS
        for subcommand, longs in GIT_ABANDON_OPTIONS.items():
            if subcommand in tokens and any(t.startswith("--") and len(t) > 2
                                            and any(option.startswith(t) for option in longs)
                                            for t in tokens):
                return True
    if "cargo" in tokens and "clean" in tokens:
        return True
    if "rsync" in tokens and any(_rsync_deletes(t) for t in tokens):  # round 23: abbreviations too
        return True
    return False


def _has_removal_form_text(text):
    """_removal_form_in as written, after NFKC folding, and after the decoding and quote removal of
    _deobfuscated."""
    import unicodedata
    folded = unicodedata.normalize("NFKC", text)
    return any(_removal_form_in(t) for t in (text, folded, _deobfuscated(text), _deobfuscated(folded)))


def _form_scan(words):
    """Deny (cannot parse) when any word holds a round 15 removal form, in its text or its raw source."""
    for text in (" ".join(w.text for w in words), " ".join(w.raw for w in words)):
        if _has_removal_form_text(text):
            return CANNOT_PARSE
    return None


def _parse_options(spec, words):
    """Skip a wrapper's options; return (index of the first operand, ok, options seen, -S value)."""
    j = 0
    seen = set()
    split = None
    while j < len(words):
        word = words[j]
        v = word.text
        if word.opaque:
            return j, False, seen, split
        if v == "--":
            return j + 1, True, seen, split
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            # Round 21 (qanorm20 F2): getopt_long accepts an unambiguous abbreviation of a long option
            # (timeout --kill=1, sudo --us, env --un, nice --adj); one that abbreviates several options of
            # one kind is read as that kind (getopt_long rejects it, so nothing runs; reading on is the
            # safe direction), and one that abbreviates options of both kinds stays unknown
            matches = _long_matches(name, spec.long_args | spec.long_flags)
            if matches and matches <= spec.long_args:
                if not eq:
                    if j + 1 >= len(words):
                        return j, False, seen, split
                    value = words[j + 1].text
                if "--split-string" in matches:
                    split = value
                seen.update(matches)
                j += 1 if eq else 2
                continue
            if matches and matches <= spec.long_flags:
                seen.update(matches)
                j += 1
                continue
            return j, False, seen, split
        if v.startswith("-") and len(v) > 1:
            cluster = v[1:]
            if spec.numeric and cluster.isdigit():
                j += 1
                continue
            step = 1
            for idx, c in enumerate(cluster):
                if c in spec.args:
                    seen.add(c)
                    value = cluster[idx + 1:]
                    if not value:
                        if j + 1 >= len(words):
                            return j, False, seen, split
                        value = words[j + 1].text
                        step = 2
                    if c == spec.split:
                        split = value
                    break
                if c in spec.optargs:
                    seen.add(c)
                    break
                if c in spec.flags:
                    seen.add(c)
                    continue
                return j, False, seen, split
            j += step
            continue
        if v == "-" and spec.dash:
            j += 1
            continue
        return j, True, seen, split
    return j, True, seen, split


def _check_wrapper(name, spec, words, depth, assigns=()):
    j, ok, seen, split = _parse_options(spec, words)
    if not ok:
        return _uncertain_scan(words)
    if name == "command" and seen & {"v", "V"}:
        return None  # command -v / -V only reports, it runs nothing
    if split is not None:
        if "${" in split and _REMOVAL_TEXT.search(_ENV_VAR_REF.sub("", split)):
            return CANNOT_PARSE  # env -S expands ${NAME}; an empty value could form a removal word
        if "\\" in split and any(_REMOVAL_TEXT.search(v) for v in (re.sub(r"\\.", " ", split),
                                                                   split.replace("\\", ""))):
            return CANNOT_PARSE  # env -S has its own escapes (\_ separates, \c ends); shlex does not
        try:
            parts = shlex.split(split)
        except ValueError:
            return _uncertain_scan(words)
        expanded = [Word.literal("env")] + [Word.literal(p) for p in parts] + list(words[j:])
        return _check_argv(expanded, depth + 1, assigns)
    if name in ("env", "sudo"):
        start = j
        while j < len(words) and "=" in words[j].text and not words[j].text.startswith("="):
            j += 1
        assigns = list(assigns) + list(words[start:j])  # round 21: NAME=VALUE that awk reads by ENVIRON
    if name == "timeout" and j < len(words):
        j += 1  # the DURATION operand
    if name == "taskset":
        if seen & {"p", "--pid"}:
            return None  # taskset -p reads or sets the mask of a running process; it runs nothing
        j += 1  # the MASK or CPU-LIST operand
    if name == "chrt":
        if seen & {"p", "m", "--pid", "--max"}:
            return None  # chrt -p reads or sets the policy of a running process, chrt -m prints limits
        if j < len(words) and not words[j].opaque and words[j].text.isdigit():
            j += 1  # the PRIORITY operand
    if name == "flock":
        return _check_flock(words[j:], depth)
    if j >= len(words):
        return None
    return _check_argv(words[j:], depth + 1, assigns)


# Round 40 (qanorm39 F2) to round 42 (qanorm41 F1) located the git command behind each program that puts
# the items it reads or the paths it finds into the command it runs, by reading that program's options,
# and checked it again with a path appended; each round found option forms that hid git. Round 43
# (qanorm42 N1 to N3, N6) dropped that modelling and denied a guarded subcommand there; rounds 43 and 44
# then read git's own options to find that subcommand, and each review found a value that hides it
# (qanorm43 B1 and M1, qanorm44 F1 a to c and F2). Round 45 (qanorm44 F1, F2) stops reading git's options
# there and uses an allowlist, the fail-safe design grc's owner chose: behind xargs, gxargs, fd and fdfind
# -x, -X, --exec and --exec-batch, find, gfind and bfs -exec, -execdir, -ok and -okdir blocks that hold
# {}, and GNU parallel, sem, xe and rush (with any wrapper before git), a git command is allowed only when
# the word right after git is a plain literal word that is one of the subcommands below; every other form
# is cannot-parse (see _appended_git_check). Each subcommand below only reads the object database, the
# refs, the index or the working tree, by git's documentation (recalled, not read in round 45 and not
# witnessed); none takes an option that runs a program named on its command line. Round 46 (qanorm45 F3):
# six of them take --output FILE, which opens FILE for writing and so can empty or replace any file the
# user may write, a tracked file, .git/index or a ref file included, as a shell redirect would: log, show,
# diff, rev-list, shortlog and blame (qanorm45 witnessed, git 2.53.0, that rev-list and blame --output=F
# left F empty and shortlog and log --output=F wrote F); the items the program reads can supply that
# option too (printf -- '--output=.git/HEAD\n' | xargs git log). They stay listed, and RESIDUAL names
# this with the programs that git's configuration or the environment names.
#   log           shows commit logs: reads commits, trees and refs
#   show          shows objects (commits, tags, trees, blobs): reads them
#   diff          shows changes between commits, the index and the working tree: reads them (git may
#                 refresh the index's cached file-stat data, which changes no staged content)
#   status        shows the working-tree status: reads it (it may refresh the index's cached file-stat
#                 data, the documented optional lock that --no-optional-locks turns off; no staged content)
#   ls-files      lists the files in the index and the working tree
#   ls-tree       lists the contents of a tree object
#   blame         shows which commit last changed each line of a file
#   cat-file      prints an object's content, type or size
#   rev-parse     parses revision names and prints repository paths and settings
#   rev-list      lists commits reachable from the commits given
#   shortlog      summarizes git log output by author
#   check-ignore  reports whether paths are excluded by the ignore rules
# Left out though often read-only: grep (its -O, --open-files-in-pager runs a program named on the command
# line on the matching files), and any subcommand with a discarding form (stash show, worktree list,
# branch, tag, config and the rest): the list holds only subcommands with no such form.
_GIT_APPENDED_ALLOWED = frozenset(("log", "show", "diff", "status", "ls-files", "ls-tree", "blame",
                                   "cat-file", "rev-parse", "rev-list", "shortlog", "check-ignore"))


def _appended_git_pieces(words):
    """Round 43: the words split at blanks and shell operators, as _PARALLEL_SPLIT splits a parallel line
    (so a quoted shell line or sh -c string is read piece by piece), each with its quotes and backslashes
    removed (_unquoted_piece); a piece that holds $ is None (an expansion: unknown), and a word that holds
    an expansion also starts with None. Round 44 (qanorm43 B1): also, for each piece, the index of the
    word it came from and its text before quote removal."""
    pieces, owners, raws = [], [], []
    for w, word in enumerate(words):
        if word.opaque:
            pieces.append(None)
            owners.append(w)
            raws.append(None)
        for piece in _PARALLEL_SPLIT.split(word.text):
            if piece:
                pieces.append(None if "$" in piece else _unquoted_piece(piece))
                owners.append(w)
                raws.append(piece)
    return pieces, owners, raws


# Round 45 (qanorm44 F2 a, b): the long options by which GNU parallel, sem, xargs, gxargs, xe and rush
# may make a word a replacement string, that is, replace it, or part of it, with each item they read
# (parallel's --replace and its *replace options, --rpl, which defines a replacement string, and --parens,
# which changes the delimiters of the {= =} expression), each matched by any prefix, as Getopt::Long
# reads an unambiguous one. Recalled from the tools' documentation, not witnessed. No value is read: a
# match, or a short-option cluster holding I, J or i (xargs -I R, -i, -0IR, BSD xargs -J R, parallel -I
# R), or an expansion before git, makes the git command cannot-parse whatever the value.
_APPENDED_REPLACE_LONG = ("replace", "replace-str", "extensionreplace", "er", "basenamereplace", "bnr",
                          "dirnamereplace", "dnr", "basenameextensionreplace", "bner", "seqreplace",
                          "slotreplace", "rpl", "parens")


def _appended_may_replace(pieces):
    """Round 45 (qanorm44 F2): whether the pieces before git (the program's own words and any wrapper's)
    may make a word after git a replacement string: an expansion (unknown), a short-option cluster that
    holds I, J or i, or a long option whose name is a prefix of one in _APPENDED_REPLACE_LONG."""
    for piece in pieces:
        if piece is None:
            return True
        if piece.startswith("--"):
            # round 46 (qanorm45 F2 b): Getopt::Long matches a long option name in any letter case
            name = piece[2:].partition("=")[0].lower()
            if name and any(opt.startswith(name) for opt in _APPENDED_REPLACE_LONG):
                return True
        elif piece.startswith("-") and set(piece[1:]) & set("IJi"):
            return True
    return False


def _appended_git_check(words):
    """Round 43 (qanorm42 N1 to N3, N6): words are those of a program that puts paths or items into the
    command it runs, its own options included (see _GIT_APPENDED_ALLOWED). No option table of the program
    is read for it. Round 45 (qanorm44 F1, F2): an allowlist, and git's options are not read. Each piece
    that names git (its last path component is git, after quote removal) is allowed only when:
      * the piece is its whole word, and that word holds no quote or backslash (a git word that is one
        piece of a quoted shell line, ls | parallel 'git log {}', is cannot-parse);
      * no piece before it may make a later word a replacement string (_appended_may_replace);
      * the word right after the git word exists and is a plain literal word, with no quoting, escaping
        or expansion, whose text is one of _GIT_APPENDED_ALLOWED.
    So any option before the subcommand (git -C x log, git '--namespace=x log' restore), any subcommand
    outside the list (an alias, git R, git :::, git {}), a missing subcommand (xargs git) and any non-literal
    word there are cannot-parse. A piece that is an expansion, which may be git (xargs $GIT restore), is
    cannot-parse when any later piece is a subcommand git ships that is outside the list; an expansion
    followed only by other words is not read (see RESIDUAL)."""
    pieces, owners, raws = _appended_git_pieces(words)
    for idx, piece in enumerate(pieces):
        if piece is None:
            if any(later is not None and later in GIT_SUBCOMMANDS and later not in _GIT_APPENDED_ALLOWED
                   for later in pieces[idx + 1:]):
                return CANNOT_PARSE
            continue
        if _basename(piece) != "git":
            continue
        w = owners[idx]
        if owners.count(w) != 1 or raws[idx] != piece or words[w].text != piece:
            return CANNOT_PARSE  # one piece of a quoted shell line, or a quote or escape in the git word
        if _appended_may_replace(pieces[:idx]):
            return CANNOT_PARSE
        if w + 1 >= len(words):
            return CANNOT_PARSE  # no subcommand: it comes from the items the program reads
        sub = words[w + 1]
        if sub.opaque or sub.quoted or sub.raw != sub.text or sub.text not in _GIT_APPENDED_ALLOWED:
            return CANNOT_PARSE
    return None


# Round 46 (qanorm45 F1, F2, F4): round 45's allowlist covered git's own words, but the guard still had
# to find git behind the path-adding program, and env -S strings, a PARALLEL= setting and a replacement
# string that becomes the command word hid it. Round 46 puts an allowlist one level up: behind xargs,
# gxargs, fd and fdfind -x, -X, --exec and --exec-batch, find, gfind and bfs -exec, -execdir, -ok and
# -okdir blocks that hold {}, and GNU parallel, sem, xe and rush, the command the program runs must
# start with a word that is exactly one of the names below, as written (no path, quote, backslash,
# expansion, assignment word or replacement string); every other command there is cannot-parse
# (_appended_command_check). Each name is a plain program that runs no command it is given: none takes
# an option or reads a setting that names a program or code to run (recalled from GNU coreutils, grep and
# diffutils documentation, not witnessed). Round 47 (qanorm46 m2): diff -l (--paginate) does start a
# program, pr, but a fixed one that runs nothing it is given (recalled, not witnessed); and (qanorm46 B2)
# a bash function exported under one of these names runs instead of the program (see RESIDUAL). git is
# on the list only under round 45's rule
# (_appended_git_check, _GIT_APPENDED_ALLOWED). Left out because they run a command or code they are
# given: env, sudo, doas, nice, nohup, time, timeout, stdbuf, setsid, flock, chroot, xargs, find, fd,
# parallel and the other path-adding programs, sh, bash and every shell, python, perl, awk, sed (its e
# command and e flag), rg (--pre, -z), sort (--compress-program), tar (--to-command,
# --use-compress-program), file (it may run a decompressor), less and more (LESSOPEN, !), vi and other
# editors, make, and every program the guard does not know.
_APPENDED_PLAIN_PROGRAMS = frozenset((
    "cat", "head", "tail", "wc", "ls", "stat", "du", "grep", "egrep", "fgrep", "echo", "printf",
    "basename", "dirname", "realpath", "readlink", "md5sum", "sha1sum", "sha224sum", "sha256sum",
    "sha384sum", "sha512sum", "b2sum", "cksum", "cut", "uniq", "nl", "od", "cmp", "diff", "touch", "chmod",
    "mkdir", "cp", "mv", "ln", "git"))
# Round 46 (qanorm45 F2 a, F5): the settings a path-adding program, the shell GNU parallel, sem and rush
# start, or a listed program reads that may change what runs: GNU parallel's PARALLEL, PARALLEL_SHELL,
# PARALLEL_HOME, PARALLEL_SSH and the rest (options, its shell, its configuration directory), git's GIT_
# variables (GIT_CONFIG_PARAMETERS, GIT_CONFIG_COUNT with GIT_CONFIG_KEY_n and GIT_CONFIG_VALUE_n,
# GIT_EXTERNAL_DIFF, GIT_PAGER, GIT_EDITOR, GIT_SSH_COMMAND, GIT_EXEC_PATH and the rest), PATH (which
# program a name finds), SHELL, BASH_ENV and ENV (the shell a program starts and the file it reads),
# HOME and XDG_CONFIG_HOME (where git and GNU parallel find their configuration), LD_ variables (code
# loaded into any program), and PAGER, LESS, LESSOPEN, EDITOR and VISUAL (programs git starts). Any
# occurrence of such a name as a whole word in the command text, not after $ or ${, counts: NAME=,
# NAME+=, and the forms that assign without = (export NAME, read NAME, declare NAME, printf -v NAME).
# Round 47 (qanorm46 M1, B2): only a name written out matches; a name built at run time (export
# "${v}EL=...", export $(cat env.txt)) and a BASH_FUNC_NAME%% function setting do not (see RESIDUAL).
_APPENDED_SETTING = re.compile(
    r"(?<![\w$])(?<!\$\{)(?:PARALLEL\w*|GIT_\w+|PATH|SHELL|BASH_ENV|ENV|HOME|XDG_CONFIG_HOME|LD_\w+|PAGER"
    r"|LESS\w*|EDITOR|VISUAL)(?!\w)")
# Round 46: the GNU parallel and sem options that name a program, perl code or a file of options (--ssh,
# --compress-program, --decompress-program, --filter, --group-by, --profile, --sshloginfile); any of
# them, in any letter case or abbreviation, makes the command cannot-parse, and so do -J (a profile)
# and xe's -s (a script sh runs). Round 47 (qanorm46 m1, M2): the set leaves out --limit, which also
# runs a command it names, and --parens, which changes the {= =} delimiters (see RESIDUAL).
_APPENDED_PROGRAM_LONG = frozenset(("--ssh", "--compress-program", "--decompress-program", "--filter",
                                    "--group-by", "--profile", "--sshloginfile", "--slf"))
# the whole command text of the hook call being checked (set by _check_command_text at depth 0)
_command_text = [""]


def _appended_parallel_start(tool, words):
    """Round 46: the index of the command word of a GNU parallel, sem, xe or rush command, read through
    PATH_APPENDERS strictly: None when an option is one the table does not settle (an unknown option or
    letter, an abbreviation of options of two kinds), names a program, code or a profile
    (_APPENDED_PROGRAM_LONG, parallel and sem -J, xe -s), or has a value that holds a blank or {=; and
    len(words) when no command word follows. Long option names of parallel and sem are matched in any
    letter case, as Getopt::Long matches them (recalled, not witnessed)."""
    spec = PATH_APPENDERS[tool]
    long_all = spec.long_args | spec.long_flags | spec.long_optargs
    fold = tool in ("parallel", "sem")
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return None
        if v == "--":
            return k + 1
        if not v.startswith("-") or v == "-":
            return k
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            matches = _long_matches(name.lower() if fold else name, long_all)
            if not matches or matches & _APPENDED_PROGRAM_LONG:
                return None
            if matches <= spec.long_args:
                if not eq:
                    if k + 1 >= len(words):
                        return None
                    value = words[k + 1].text
                    k += 1
            elif not (matches <= spec.long_flags or matches <= spec.long_optargs):
                return None
            if any(c.isspace() for c in value) or "{=" in value:
                return None
            k += 1
            continue
        for idx in range(1, len(v)):
            c = v[idx]
            if (fold and c == "J") or (tool == "xe" and c == "s"):
                return None
            if c in spec.flags:
                continue
            if c in spec.args:
                value = v[idx + 1:]
                if not value:
                    if k + 1 >= len(words):
                        return None
                    value = words[k + 1].text
                    k += 1
                if any(ch.isspace() for ch in value) or "{=" in value:
                    return None
                break
            if c in spec.optargs:
                break
            return None
        k += 1
    return len(words)


def _appended_command_check(words, start, shell_line=False):
    """Round 46 (qanorm45 F1, F2, F4): words are those of a path-adding program (its own options
    included) and start is the index of the command it runs (None when its options are not settled; at
    or past the end when it names none). CANNOT_PARSE unless:
      * a command word exists, is a plain literal word (no quote, backslash, expansion or substitution)
        and its text is one of _APPENDED_PLAIN_PROGRAMS exactly (so env -S..., sudo, sh -c, an assignment
        word, a path, {}, % and gi% are cannot-parse);
      * when a piece before it may name a replacement string (_appended_may_replace), no piece before it
        is an expansion and no ending of a piece before it (where an attached or separate replacement
        string sits) occurs inside the command word (xargs -I gr grep, xargs -Igr grep);
      * with shell_line (GNU parallel, sem, rush and xe, which may join their command into a shell line),
        the first word of each part of that line before the first input-source separator, after a shell
        operator, $( or a backquote, is also on the list (parallel grep x '{};' env ...);
      * the command text holds no setting such a program reads (_APPENDED_SETTING), anywhere.
    The caller still applies _appended_git_check, so git keeps round 45's rule."""
    if start is None or start >= len(words):
        return CANNOT_PARSE
    word = words[start]
    if word.opaque or word.quoted or word.raw != word.text or word.text not in _APPENDED_PLAIN_PROGRAMS:
        return CANNOT_PARSE
    before = _appended_git_pieces(words[:start])[0]
    if _appended_may_replace(before):
        for piece in before:
            if piece is None or any(piece[i:] in word.text for i in range(len(piece))):
                return CANNOT_PARSE
    if shell_line:
        end = start
        while end < len(words) and words[end].text not in _PARALLEL_SEPARATORS:
            end += 1
        if any(w.opaque or "{=" in w.text for w in words):
            return CANNOT_PARSE
        if any(head not in _APPENDED_PLAIN_PROGRAMS for head in _parallel_heads(words[start:end])):
            return CANNOT_PARSE
    text = _command_text[0]
    if any(_APPENDED_SETTING.search(t) for t in (text, _unquoted_piece(text))):
        return CANNOT_PARSE
    return None


def _check_path_appender(argv, depth, assigns=()):
    """Round 41 (qanorm40 N1): the argv check of a command run by a program that adds paths to it (fd and
    find exec blocks), then, when that finds nothing, round 46's _appended_command_check (the block is
    the command, so its first word is the command word) and round 43's _appended_git_check."""
    result = _check_argv(argv, depth + 1, assigns)
    if result is not None:
        return result
    if not argv:
        return None
    return _appended_command_check(argv, 0) or _appended_git_check(argv)


def _check_flock(words, depth):
    """flock FILE COMMAND [ARG]... runs COMMAND, and flock FILE -c STRING runs STRING with sh -c; flock
    FD alone runs nothing."""
    if len(words) < 2:
        return None
    following = words[1]
    if following.text in ("-c", "--command"):
        return _check_command_word(words[2:], depth) if len(words) > 2 else None
    if following.text.startswith("--command="):
        string = following.text.partition("=")[2]
        return _check_command_word([Word(string, following.raw, following.quoted, following.opaque)], depth)
    return _check_argv(words[1:], depth + 1)


def _check_command_word(words, depth):
    """The first word is a command string that a shell runs (sh -c STRING, flock FILE -c STRING): check it
    as a command. An expansion in it makes the string unknown: deny (cannot parse) when the words hold a
    removal word."""
    if not words:
        return None
    target = words[0]
    # Round 16 (qanorm15 M2): a string it cannot read also denies when it holds a round 15 removal form
    result = _check_command_text(target.text, depth + 1, True)
    if result == DENY:
        return DENY
    # Round 18 (qanorm17 MD3): a string that runs its later arguments ("$@", $0 to $9)
    passed = _passed_arguments(_SHELL_ARGS, target.text, words[1:], depth)
    if passed == DENY:
        return DENY
    result = result or passed
    if target.opaque:
        return _uncertain_scan(words) or _form_scan(words) or result
    return result


# Round 18 (qanorm17 MD3): a program that passes its later arguments on: a shell string's "$@", $*, $0 to
# $9 (also in braces), a python program's sys.argv (or argv), a perl program's @ARGV. Round 19 (qanorm18
# MEDIUM-3): also a shell string's for or select NAME with no in list (it loops over "$@"), ${!#} (the
# last argument) and BASH_ARGV, each read as naming any later word; python's sys.orig_argv; and perl's
# shift and pop, which take from @ARGV outside a sub.
_SHELL_ARGS = re.compile(r"\$\{?([@*0-9])|\$\{!#\}|BASH_ARGV|(?<![A-Za-z0-9_])(?:for|select)[ \t]+"
                         r"[A-Za-z_][A-Za-z0-9_]*[ \t]*(?:;|\n|do(?![A-Za-z0-9_]))")
_PY_ARGS = re.compile(r"(?<![A-Za-z0-9_])(?:orig_)?argv(?![A-Za-z0-9_])")
_PERL_ARGS = re.compile(r"(?<![A-Za-z0-9_])(?:ARGV|shift|pop)(?![A-Za-z0-9_])")


def _passed_arguments(pattern, program, later, depth):
    """When the program text refers to its later arguments, read them as a command: from each argument
    a reference names ($0 the first later word, "$@", $* and $1 the second, for a shell; the first for
    python and perl), and deny (cannot parse) when an unquoted later word is a removal command name or
    git with a removal form, as for a command word the guard does not know. Round 20 (gemnorm19 BLOCKER):
    a cannot-parse from that argv check propagates. Round 20 (qanorm19 MEDIUM-1): a later word, quoted
    or not, that holds a removal word or a round 15 removal form denies as cannot-parse, since the program
    may run it as one command string (sh -c '$1' _ 'rm -rf x', os.system(sys.argv[1]))."""
    if not later or depth > MAX_CHECK_DEPTH:
        return None
    starts = set()
    for match in pattern.finditer(program):
        ref = match.group(1) if pattern.groups else ""
        if ref is None:
            starts.update(range(len(later)))  # round 19: a reference that may name any later word
            continue
        starts.add(int(ref) if ref.isdigit() else (1 if ref in ("@", "*") else 0))
    if not starts:
        return None
    result = None
    for start in sorted(starts):
        if start < len(later):
            got = _check_argv(later[start:], depth + 1)
            if got == DENY:
                return DENY
            result = result or got
    if any(_has_removal_text(w.text) or _has_removal_text(w.raw) for w in later):
        return CANNOT_PARSE
    return result or _form_scan(later) or _unknown_command_scan(later, depth)


# Round 18 (qanorm17 m3): the long options of su (util-linux) and fish, each of which accepts an
# unambiguous abbreviation of one (getopt_long).
_SU_LONG = frozenset(("--command", "--session-command", "--shell", "--group", "--supp-group",
                      "--whitelist-environment", "--login", "--preserve-environment", "--pty", "--fast",
                      "--help", "--version"))
_FISH_LONG = frozenset(("--command", "--init-command", "--debug", "--debug-output", "--debug-stack-frames",
                        "--features", "--interactive", "--login", "--no-config", "--no-execute",
                        "--print-rusage-self", "--print-debug-categories", "--profile", "--profile-startup",
                        "--private", "--help", "--version"))


def _long_matches(name, options):
    """The long options that name is or abbreviates: itself when exact, else every option it starts."""
    if name in options:
        return {name}
    if len(name) <= 2:
        return set()
    return {option for option in options if option.startswith(name)}


def _check_su(words, depth):
    """su [OPTIONS] [-] [USER [ARG]...] with -c, --command or --session-command runs COMMAND with the
    user's shell (after USER too, where the shell reads -c): check it as a shell -c string. An expansion
    may become -c: deny (cannot parse) when the words hold a removal word or form."""
    result = None
    opaque = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            opaque = True
            k += 1
            continue
        command = None
        step = 1
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            # Round 18 (qanorm17 m3): su accepts an unambiguous abbreviation; an ambiguous one that may
            # be a command option is read as one (the safe direction)
            matches = _long_matches(name, _SU_LONG)
            if matches & {"--command", "--session-command"}:
                if eq:
                    command = Word(value, word.raw, word.quoted, word.opaque)
                elif k + 1 < len(words):
                    command = words[k + 1]
                    step = 2
            elif matches and matches <= {"--shell", "--group", "--supp-group", "--whitelist-environment"} \
                    and not eq:
                step = 2
        elif v.startswith("-") and len(v) > 1:
            cluster = v[1:]
            for idx, c in enumerate(cluster):
                value = cluster[idx + 1:]
                if c == "c":
                    if value:
                        command = Word(value, value)
                    elif k + 1 < len(words):
                        command = words[k + 1]
                        step = 2
                    break
                if c in "sgGw":
                    if not value:
                        step = 2
                    break
        if command is not None:
            got = _check_command_word([command], depth)
            if got == DENY:
                return DENY
            result = result or got
        k += step
    if opaque and result is None:
        return _uncertain_scan(words) or _form_scan(words)
    return result


def _check_jobs(words, depth):
    """Round 17 (qanorm16 F2): bash's jobs -x COMMAND [ARG]... puts a process group ID in place of each
    jobspec in its words and runs COMMAND: check it as a command. Without -x jobs only lists. An expansion
    among its options may become -x: deny (cannot parse) when the words hold a removal word or form."""
    execute = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return _uncertain_scan(words) or _form_scan(words)
        if v == "--":
            k += 1
            break
        if v.startswith("-") and len(v) > 1:
            execute = execute or "x" in v[1:]
            k += 1
            continue
        break
    if not execute or k >= len(words):
        return None
    return _check_argv(words[k:], depth + 1)


# Round 20 (qanorm19 MINOR-1): ssh [OPTIONS] HOST [OPTIONS] [COMMAND [ARG]...] joins COMMAND and its args
# with spaces and has the remote user's shell run that string; with no command (and no -n, -N, -f, -W,
# -O, -G, -Q, -V or -s) that shell reads its commands from ssh's standard input.
_SSH_FLAGS = "46AaCfGgKkMNnqsTtVvXxYy"
_SSH_VALUES = "BbcDEeFIiJLlmOoPpQRSWw"
_SSH_NO_STDIN_SHELL = frozenset("nNfWOGQVs")


def _ssh_parse(words):
    """(ok, option letters seen, remote command words). ok is False when an expansion or an option the
    guard does not know leaves the host or the command unknown."""
    seen = set()
    host_seen = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return False, seen, words[k:]
        if v == "--":
            k += 1
            if not host_seen and k < len(words):
                host_seen = True
                k += 1
            break
        if v.startswith("-") and len(v) > 1:
            step = 1
            for idx, c in enumerate(v[1:]):
                if c in _SSH_VALUES:
                    seen.add(c)
                    if not v[idx + 2:]:
                        step = 2
                    break
                if c in _SSH_FLAGS:
                    seen.add(c)
                    continue
                return False, seen, words[k:]
            k += step
            continue
        if host_seen:
            break
        host_seen = True
        k += 1
    return True, seen, (words[k:] if host_seen else [])


def _check_ssh(words, depth):
    """ssh with a remote command: check the command string the remote shell runs (its words joined with
    spaces), as a shell -c string. An expansion or an option it does not know: deny (cannot parse) when a
    removal word or a round 15 removal form follows."""
    ok, _seen, command = _ssh_parse(words)
    if not ok:
        return _uncertain_scan(words) or _form_scan(words)
    if not command:
        return None
    result = _check_command_text(" ".join(w.text for w in command), depth + 1, True)
    if result == DENY:
        return DENY
    if any(w.opaque for w in command):
        return _uncertain_scan(command) or _form_scan(command) or result
    return result


# Round 20 (qanorm19 MINOR-1): an awk program that runs a shell command (system(), or a | pipe to or from a
# command string) and a sed script with the e command or the s///e flag, when it also holds a removal word
# or a round 15 removal form, deny as cannot-parse (a text test; the guard does not parse awk or sed). awk
# -f FILE and sed -f FILE read a program file, which counts as a program read from stdin when it is -,
# /dev/stdin, /dev/fd/N or a process substitution (see _program_source).
_AWK_SHELL = re.compile(r"(?<![A-Za-z0-9_])system[ \t]*\(|(?<!\|)\|(?!\|)")
_AWK_VALUE_SHORT = "FvfeEilW"
_AWK_VALUE_LONG = frozenset(("--field-separator", "--assign", "--file", "--source", "--exec", "--include",
                             "--load"))
_SED_EXEC = re.compile(r"(?<![A-Za-z0-9_\\])[gpIiMm0-9]*e[gpIiMm0-9]*(?![A-Za-z0-9_])")


def _option_value(words, k, value, attached):
    """The value word of an option: the attached text, else the next word (None when there is none)."""
    if attached:
        return Word.literal(value), 1
    return (words[k + 1] if k + 1 < len(words) else None), 2


def _awk_programs(words):
    """(program words, program file words, data words) of an awk argv; programs is None when an
    expansion leaves them unknown. Round 21 (qanorm20 F1): the data words are the -v and --assign
    values and the operands after the program, which the program reads as variables or ARGV."""
    programs, files, data = [], [], []
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return None, files, data
        if v == "--":
            k += 1
            break
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            if name in _AWK_VALUE_LONG:
                target, step = _option_value(words, k, value, bool(eq))
                if target is not None and name == "--source":
                    programs.append(target)
                elif target is not None and name in ("--file", "--exec"):
                    files.append(target)
                elif target is not None and name == "--assign":
                    data.append(target)
                k += step
                continue
            k += 1
            continue
        if v.startswith("-") and len(v) > 1:
            c = v[1]
            if c in _AWK_VALUE_SHORT:
                target, step = _option_value(words, k, v[2:], bool(v[2:]))
                if target is not None and c == "e":
                    programs.append(target)
                elif target is not None and c in "fE":
                    files.append(target)
                elif target is not None and c == "v":
                    data.append(target)
                k += step
                continue
            k += 1  # a flag (also gawk's optional attached values)
            continue
        break
    if not programs and not files and k < len(words):
        programs.append(words[k])
        k += 1
    data.extend(words[k:])
    return programs, files, data


def _sed_programs(words):
    """(script words, script file words, --sandbox given) of a sed argv; scripts is None when an
    expansion leaves them unknown."""
    programs, files = [], []
    sandbox = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return None, files, sandbox
        if v == "--":
            k += 1
            break
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            kind = None
            if len(name) > 2 and "--expression".startswith(name):
                kind = "e"
            elif len(name) > 3 and "--file".startswith(name):
                kind = "f"
            elif len(name) > 2 and "--line-length".startswith(name):
                kind = "l"
            if kind is not None:
                target, step = _option_value(words, k, value, bool(eq))
                if target is not None and kind == "e":
                    programs.append(target)
                elif target is not None and kind == "f":
                    files.append(target)
                k += step
                continue
            sandbox = sandbox or (len(name) > 3 and "--sandbox".startswith(name))
            k += 1
            continue
        if v.startswith("-") and len(v) > 1:
            step = 1
            for idx, c in enumerate(v[1:]):
                if c in "efl":
                    target, step = _option_value(words, k, v[idx + 2:], bool(v[idx + 2:]))
                    if target is not None and c == "e":
                        programs.append(target)
                    elif target is not None and c == "f":
                        files.append(target)
                    break
                if c == "i":
                    break  # -i[SUFFIX]
            k += step
            continue
        break
    if not programs and not files and k < len(words):
        programs.append(words[k])
    return programs, files, sandbox


def _program_runs_removal(programs, words, shell_call, data=()):
    """Deny (cannot parse) when a program word runs a shell command (shell_call matches its text) and
    holds a removal word or a round 15 removal form, or is an expansion next to one. Round 21 (qanorm20
    F1): the data words count as program text then (awk -v cmd='rm x' 'BEGIN{system(cmd)}')."""
    if programs is None:
        return _uncertain_scan(words) or _form_scan(words)
    for program in programs:
        if program.opaque:
            if _uncertain_scan([program]) or _form_scan([program]):
                return CANNOT_PARSE
            continue
        if not shell_call.search(program.text):
            continue
        for text in ("\n".join([program.text] + [w.text for w in data]),
                     "\n".join([program.raw] + [w.raw for w in data])):
            if _has_removal_text(text) or _has_removal_form_text(text):
                return CANNOT_PARSE
    return None


def _check_awk(words, assigns=()):
    """Round 21 (qanorm20 F1): when the program runs a command (system(), a pipe, or getline from a
    command), its -v and --assign values, the operands after it and the NAME=VALUE words before awk (also
    those env or sudo passes on), which it reads as variables, ARGV or ENVIRON, count as its text."""
    programs, _files, data = _awk_programs(words)
    return _program_runs_removal(programs, words, _AWK_SHELL, list(data) + list(assigns))


def _check_sed(words):
    programs, _files, sandbox = _sed_programs(words)
    if sandbox:
        return None  # sed --sandbox rejects the e command
    return _program_runs_removal(programs, words, _SED_EXEC)


def _check_fish(words, depth):
    """Round 17 (qanorm16 F4): fish -c STRING, --command STRING, -C STRING and --init-command STRING (each
    also attached, with =, or ending a cluster such as -ic or -iC) run STRING; -C and --init-command run it
    before a later -c. Check each as a command string. fish may take a value for an option this guard does
    not model, so every later word is read as a possible option (the safe direction). An expansion may
    become one of these options: deny (cannot parse) when the words hold a removal word."""
    result = None
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            # round 18 (qanorm17 m2): a round 15 removal form after it denies too, as for su
            result = result or _uncertain_scan(words[k:]) or _form_scan(words[k:])
            k += 1
            continue
        if v == "--":
            break
        string = None
        step = 1
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            if _long_matches(name, _FISH_LONG) & SHELL_COMMAND_LONG:  # round 18 (qanorm17 m3)
                if eq:
                    string = [Word(value, word.raw, word.quoted, word.opaque)]
                else:
                    string = words[k + 1:]
                    step = 2
        elif v.startswith("-") and len(v) > 1:
            for idx, c in enumerate(v[1:]):
                if c in "cC":
                    value = v[idx + 2:]
                    if value:
                        string = [Word(value, word.raw, word.quoted, word.opaque)]
                    else:
                        string = words[k + 1:]
                        step = 2
                    break
        if string:
            got = _check_command_word(string, depth)
            if got == DENY:
                return DENY
            result = result or got
        k += step
    return result


def _check_shell(words, depth):
    """bash, sh, dash or zsh given -c (alone or in a cluster such as -ec or -lc) runs its first operand as
    a command string: check it as one, with this bash grammar. Without -c that operand is a script file,
    which the guard never sees (see RESIDUAL)."""
    command = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            break
        if v in ("-", "--"):
            k += 1
            break
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            if name in SHELL_COMMAND_LONG:
                # Round 16 (qanorm15 B2): fish --command STRING (or --init-command), also with =
                if eq:
                    return _check_command_word([Word(value, word.raw, word.quoted, word.opaque)], depth)
                return _check_command_word(words[k + 1:], depth)
            k += 2 if v in SHELL_VALUE_LONG else 1
            continue
        if v[:1] in ("-", "+") and len(v) > 1:
            command = command or "c" in v[1:]
            k += 1 + sum(1 for c in v[1:] if c in "oO")  # -o NAME and -O NAME take the next word
            continue
        break
    if k >= len(words):
        return None
    if not command:
        # an expansion may become -c; round 18 (qanorm17 m2): so may a round 15 removal form, as for su
        return (_uncertain_scan(words[k:]) or _form_scan(words[k:])) if words[k].opaque else None
    return _check_command_word(words[k:], depth)


def _check_perl(words, depth=0):
    """perl -e and -E run their value as a program: deny when one holds the word unlink or rmtree (a text
    test; it does not parse perl). A script file or a program on stdin is not seen (see RESIDUAL)."""
    programs = []
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return _uncertain_scan(words[k:])
        if v in ("-", "--") or not v.startswith("-"):
            # Round 18 (qanorm17 MD3): a -e program that runs @ARGV runs the later words
            later = words[k + 1:] if v in ("-", "--") else words[k:]
            result = None
            for program in programs:
                got = _passed_arguments(_PERL_ARGS, program, later, depth)
                if got == DENY:
                    return DENY
                result = result or got
            return result
        cluster = v[1:]
        step = 1
        idx = 0
        while idx < len(cluster):
            c = cluster[idx]
            if c in "eE":
                program = cluster[idx + 1:]
                if program:
                    target = Word(program, program)
                elif k + 1 < len(words):
                    target = words[k + 1]
                    step = 2
                else:
                    return None
                if _PERL_REMOVAL.search(target.text):
                    return DENY
                # Round 16 (qanorm15 M2): a shell call (system, exec, qx, readpipe or a backquote) with a
                # removal word or a round 15 removal form, as the python rule
                if _PERL_SHELL_CALL.search(target.text) and (_REMOVAL_TEXT.search(target.text)
                                                             or _has_removal_form_text(target.text)):
                    return DENY
                if target.opaque and (_uncertain_scan([target]) or _form_scan([target])):
                    return CANNOT_PARSE
                programs.append(target.text)
                break
            if c in "0l":
                idx += 1
                digits = "01234567"
                if c == "0" and cluster[idx:idx + 1] in ("x", "X"):
                    idx += 1
                    digits = "0123456789abcdefABCDEF"
                while idx < len(cluster) and cluster[idx] in digits:
                    idx += 1
                continue
            if c in PERL_REST_VALUE:
                if (c in "IMm" and idx + 1 == len(cluster) and k + 1 < len(words)
                        and not words[k + 1].text.startswith("-")):
                    step = 2  # -I DIR or -M MODULE given as a separate word
                break
            if c in PERL_FLAGS:
                idx += 1
                continue
            return _uncertain_scan(words)  # an option it does not know
        k += step
    return None


# Round 23 (qanorm22 F3): the rsync long options that delete files. rsync accepts an unambiguous prefix
# of a long option, and no other rsync long option starts with --dele or --remov (--delay-updates and
# --remote-option stop at --del and --rem), so every prefix of these from --dele or --remov on deletes.
RSYNC_DELETE_LONG = ("--delete", "--delete-before", "--delete-during", "--delete-delay", "--delete-after",
                     "--delete-excluded", "--delete-missing-args", "--remove-source-files",
                     "--remove-sent-files")


def _rsync_deletes(name):
    """Whether an rsync long option name (before any =) deletes: --del, any --delete-* option, or an
    abbreviation of a deleting option from --dele or --remov on (--delet, --remove-so)."""
    if name == "--del" or name.startswith(("--delete", "--remove-s")):
        return True
    return name.startswith(("--dele", "--remov")) and any(opt.startswith(name) for opt in RSYNC_DELETE_LONG)


def _check_rsync(words):
    """rsync --delete (and its --delete-* and --del forms) deletes files at the destination, and
    --remove-source-files (or the older --remove-sent-files) deletes the sent source files: deny, even
    in a dry run; (round 23) also an abbreviation of one of them (--delet, --remov)."""
    for word in words:
        v = word.text
        if v == "--":
            break
        name = v.partition("=")[0]
        if _rsync_deletes(name):
            return DENY
    return None


def _check_cargo(words):
    """cargo clean deletes the target directory: deny, after the cargo options it knows, unless its only
    argument is -h or --help."""
    k = 0
    if words and not words[0].opaque and words[0].text.startswith("+"):
        k = 1  # a rustup +toolchain
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque or not v.startswith("-"):
            break
        name, eq, _value = v.partition("=")
        if name in CARGO_VALUE_OPTIONS:
            k += 1 if eq else 2
            continue
        if v in CARGO_PLAIN_OPTIONS:
            k += 1
            continue
        break  # an option it does not know may take the next word as its value
    if k >= len(words):
        return None
    if words[k].opaque or words[k].text.startswith("-"):
        return DENY if any(w.text == "clean" for w in words[k:]) else None
    if words[k].text != "clean":
        return None
    rest = words[k + 1:]
    if len(rest) == 1 and rest[0].text in ("-h", "--help"):
        return None  # it only prints
    return DENY


def _check_uv(words, depth):
    """uv run [OPTIONS] COMMAND runs COMMAND: check it, after the uv options it knows. uv run -m, -s,
    --module, --script or --gui-script runs a module or a script file, which the guard does not see."""
    j, ok, _seen, _split = _parse_options(_UV_SPEC, words)
    if not ok:
        return _uncertain_scan(words)
    if j >= len(words) or words[j].text != "run":
        return None
    rest = words[j + 1:]
    j, ok, seen, _split = _parse_options(_UV_SPEC, rest)
    if not ok:
        return _uncertain_scan(rest)
    if seen & {"m", "s", "--module", "--script", "--gui-script"}:
        return None
    if j >= len(rest):
        return None
    return _check_argv(rest[j:], depth + 1)


def _check_runner(spec, words, depth):
    """pipx run and poetry run: [OPTIONS] run [OPTIONS] COMMAND runs COMMAND. Check it after the options
    the guard knows; an option it does not know denies as cannot-parse when a removal word follows."""
    j, ok, _seen, _split = _parse_options(spec, words)
    if not ok:
        return _uncertain_scan(words)
    if j >= len(words) or words[j].text != "run":
        return None
    rest = words[j + 1:]
    j, ok, _seen, _split = _parse_options(spec, rest)
    if not ok:
        return _uncertain_scan(rest)
    if j >= len(rest):
        return None
    return _check_argv(rest[j:], depth + 1)


def _ambiguous_exec(words, is_exec):
    """After a word that may take the next word as its value, the guard cannot tell whether a later exec
    word starts a block: deny (cannot parse) when one follows and a removal word follows too."""
    if any(is_exec(w.text) for w in words):
        return _uncertain_scan(words)
    return None


def _check_find(words, depth, bfs=False):
    """find runs the command after -exec, -execdir, -ok or -okdir, up to a ';' word; GNU find also ends
    -exec and -execdir (never -ok or -okdir) at a '+' word right after a word that holds {}. An
    expansion in the block may become ';', {} or several words, so the end is unknown: deny (cannot
    parse) when a removal word follows it. The value of an option that takes one (find . -name -exec
    ...) is skipped as that value; an unquoted expansion in that value may become no word or several.
    Round 42 (qanorm41 F5): gfind and bfs are read here too; for bfs, -rm is -delete."""
    uncertain = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if v == "-delete" or (bfs and v == "-rm"):
            return DENY
        if v in FIND_EXEC:
            m = k + 1
            unsure = None
            while m < len(words) and words[m].text != ";":
                if (words[m].text == "+" and v in ("-exec", "-execdir") and m > k + 1
                        and "{}" in words[m - 1].text):
                    break
                if words[m].opaque and unsure is None:
                    unsure = m
                m += 1
            if unsure is not None:
                scanned = _uncertain_scan(words[unsure:])
                if scanned:
                    return scanned
            # round 41 (qanorm40 N1): find puts the paths it finds where {} is; the block gets the check of a
            # path-adding program's command (_check_path_appender; round 43: _appended_git_check after the
            # argv check). Round 42 (qanorm41 F3): only a block that holds
            # {} (or a word an expansion may turn into {}) gets a path from find; one without appends
            # nothing (find . -exec git checkout -m ';' runs git checkout -m alone), so it gets the argv
            # check only
            block = words[k + 1:m]
            if any("{}" in w.text or w.opaque for w in block):
                result = _check_path_appender(block, depth)
            else:
                result = _check_argv(block, depth + 1)
            if result == DENY:
                return DENY
            if result is not None:
                uncertain = True
            k = m + 1
            continue
        count = FIND_VALUE_OPTIONS.get(v, 1 if _FIND_NEWER_XY.match(v) else 0)
        if count:
            if any(w.opaque and not w.quoted for w in words[k + 1:k + 1 + count]):
                # a value that becomes no word shifts a later -delete into primary position too
                scanned = _ambiguous_exec(words[k + 1:], lambda t: t in FIND_EXEC or t == "-delete")
                if scanned:
                    return scanned
            k += 1 + count
            continue
        if not word.opaque and v.startswith("-") and len(v) > 1 and v not in FIND_PLAIN_OPTIONS:
            scanned = _ambiguous_exec(words[k + 1:], lambda t: t in FIND_EXEC)
            if scanned:
                return scanned
        k += 1
    return CANNOT_PARSE if uncertain else None


def _fd_is_exec(text):
    return text in FD_EXEC or bool(_FD_ATTACHED_EXEC.match(text))


def _fd_option_kind(word):
    """'value' for an fd option word whose value is the next word, 'unknown' for an option word the
    guard does not know (it may take a value), else 'plain'."""
    v = word.text
    if word.opaque or not v.startswith("-") or v in ("-", "--"):
        return "plain"
    if v.startswith("--"):
        name, eq, _value = v.partition("=")
        if name in FD_VALUE_LONG:
            return "plain" if eq else "value"
        return "plain" if name in FD_PLAIN_LONG else "unknown"
    for idx, c in enumerate(v[1:]):
        if c in FD_VALUE_SHORT:
            return "plain" if v[idx + 2:] else "value"
        if c not in FD_PLAIN_SHORT:
            return "unknown"
    return "plain"


def _check_fd(words, depth):
    """fd -x/--exec and -X/--exec-batch run the command that follows, up to a ';' word. Every exec
    option is judged: one that removes denies, whatever the others run. The value of an option that
    takes one is skipped as that value; fd may refuse a value that starts with - and read it as an
    option, so a value that is an exec option is ambiguous."""
    uncertain = False
    k = 0
    while k < len(words):
        word = words[k]
        if word.text in FD_EXEC:
            m = k + 1
            while m < len(words) and words[m].text != ";":
                m += 1
            # round 41 (qanorm40 N1): with no placeholder ({}, {/}, {//}, {.}, {/.}) fd appends the path it
            # found to the command (inference from fd's documentation, not witnessed); the command gets
            # _check_path_appender (round 43: _appended_git_check after the argv check)
            result = _check_path_appender(words[k + 1:m], depth)
            if result == DENY:
                return DENY
            if result is not None:
                uncertain = True
            k = m + 1
            continue
        attached = _FD_ATTACHED_EXEC.match(word.text)
        if attached:  # --exec=CMD or -xCMD: an attached form it does not split
            scanned = _uncertain_scan([Word.literal(word.text[attached.end():])] + list(words[k:]))
            # round 42 (qanorm41 F1): the command it may run, through _check_path_appender; a finding
            # denies as cannot-parse (fd --exec=git restore --theirs)
            m = k + 1
            while m < len(words) and words[m].text != ";":
                m += 1
            rest_text = word.text[attached.end():]
            appended = _check_path_appender(
                ([Word(rest_text, word.raw, word.quoted, word.opaque)] if rest_text else [])
                + list(words[k + 1:m]), depth)
            return scanned or (CANNOT_PARSE if uncertain or appended is not None else None)
        kind = _fd_option_kind(word)
        if kind == "value":
            if k + 1 < len(words) and _fd_is_exec(words[k + 1].text):
                scanned = _uncertain_scan(words[k + 1:])
                if scanned:
                    return scanned
                # round 42 (qanorm41 F1): fd may read that exec word as the exec option; its command
                # denies as cannot-parse when _check_path_appender finds anything
                m = k + 2
                while m < len(words) and words[m].text != ";":
                    m += 1
                if _check_path_appender(words[k + 2:m], depth) is not None:
                    return CANNOT_PARSE
            k += 2
            continue
        if kind == "unknown":
            scanned = _ambiguous_exec(words[k + 1:], _fd_is_exec)
            if scanned:
                return scanned
        k += 1
    return CANNOT_PARSE if uncertain else None


def _check_git(words, depth):
    """git rm deletes the named tracked files from the working tree. Without -f git refuses a file whose
    content differs from HEAD (a residual: HEAD holds what it removes); with -f or --force and no
    --cached it can delete content no commit holds, so it denies. git parses options anywhere before --,
    and an expansion there may become -f, --force or --no-cached: deny (cannot parse)."""
    k = 0
    autocorrect = False
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque or not v.startswith("-") or v == "-":
            break
        name, eq, _value = v.partition("=")
        if v in ("-C", "-c") or (name in GIT_VALUE_OPTIONS and name.startswith("--")):
            # Round 21 (qanorm20 F3): -c help.autocorrect=... (also --config-env) makes git run the
            # subcommand it takes a mistyped word for
            if v == "-c" or name == "--config-env":
                setting = _value if eq else (words[k + 1].text if k + 1 < len(words) else "")
                autocorrect = autocorrect or setting.partition("=")[0].lower() == "help.autocorrect"
            k += 1 if eq and name.startswith("--") else 2
            continue
        if v in GIT_PLAIN_OPTIONS or name == "--exec-path":
            k += 1
            continue
        return _uncertain_scan(words)  # an option it does not know may take the next word as its value
    if k >= len(words):
        return None
    if autocorrect:
        return CANNOT_PARSE  # round 21 (qanorm20 F3): git may run another subcommand than the one named
    if words[k].opaque:
        return _uncertain_scan(words[k:])  # a subcommand built at run time
    subcommand = words[k].text
    if subcommand not in GIT_SUBCOMMANDS:
        # Round 21 (qanorm20 F3): an alias, a git-WORD program or, with help.autocorrect set in the
        # configuration, a mistyped subcommand: deny (cannot parse) when the git argv holds a removal word
        # or a round 15 removal form
        return _uncertain_scan(words) or _form_scan([Word.literal("git")] + list(words))
    if subcommand == "config" and any(w.text.partition("=")[0].lower() == "help.autocorrect"
                                      for w in words[k + 1:]):
        return CANNOT_PARSE  # round 21 (qanorm20 F3): it sets (or reads) help.autocorrect
    if subcommand == "clean":
        return _check_git_clean(words[k + 1:])
    if subcommand == "worktree":
        return _check_git_worktree(words[k + 1:])
    if subcommand == "reset":
        return _check_git_reset(words[k + 1:])
    if subcommand == "stash":
        return _check_git_stash(words[k + 1:])
    if subcommand == "checkout":
        return _check_git_checkout(words[k + 1:])
    if subcommand == "restore":
        return _check_git_restore(words[k + 1:])  # round 39 (qanorm38 F1)
    # Round 16 (qanorm15 MN3, M1): git switch -f, and the subcommands that run a command
    if subcommand == "switch":
        return _check_git_switch(words[k + 1:])
    if subcommand == "submodule":
        return _check_git_submodule(words[k + 1:], depth)
    if subcommand == "bisect":
        return _check_git_bisect(words[k + 1:], depth)
    if subcommand == "read-tree":
        return _check_git_read_tree(words[k + 1:])
    if subcommand == "checkout-index":
        # Round 18 (qanorm17 MD2): git checkout-index -f or --force overwrites existing working-tree files
        return _git_force_option(words[k + 1:], "f", ("--force",))
    if subcommand in GIT_ABANDON_OPTIONS and _check_git_abandon(words[k + 1:],
                                                                GIT_ABANDON_OPTIONS[subcommand]) == DENY:
        return DENY  # round 31 (qanorm30 MINOR-1); otherwise git rebase goes on to its --exec check
    if subcommand in GIT_COMMAND_OPTIONS:
        return _check_git_command_options(GIT_COMMAND_OPTIONS[subcommand], words[k + 1:], depth)
    if subcommand != "rm":
        return None
    force = False
    cached = False
    for word in words[k + 1:]:
        v = word.text
        if word.opaque:
            return CANNOT_PARSE
        if v == "--":
            break
        if v.startswith("--"):
            name = v.partition("=")[0]
            if len(name) > 2 and "--force".startswith(name):
                force = True
            elif v == "--cached":
                cached = True
            elif name.startswith("--no-"):
                cached = False  # --no-cached, or an abbreviation of it: the safe direction
        elif v.startswith("-") and "f" in v[1:]:
            force = True
    return DENY if force and not cached else None


def _check_git_clean(words):
    """git clean deletes untracked files (with -x also ignored ones; with clean.requireForce false even
    without -f): deny every form but a dry run (-n or --dry-run, with no later --no- option) and the help
    forms (git clean -h, git clean --help). An expansion before -- may become --no-dry-run: deny."""
    if len(words) == 1 and words[0].text in ("-h", "--help"):
        return None  # it only prints
    dry = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return DENY
        if v == "--":
            break
        if v.startswith("--"):
            name, eq, _value = v.partition("=")
            if len(name) > 2 and "--dry-run".startswith(name):
                dry = True  # round 16 (qanorm15 MN2): git accepts --d to --dry-ru for --dry-run
            elif name.startswith("--no-"):
                dry = False  # --no-dry-run, or an abbreviation of it: the safe direction
            elif len(name) > 2 and "--exclude".startswith(name) and not eq:
                k += 1  # its PATTERN
        elif v.startswith("-") and len(v) > 1:
            for idx, c in enumerate(v[1:]):
                if c == "e":
                    if not v[idx + 2:]:
                        k += 1  # -e PATTERN
                    break
                if c == "n":
                    dry = True
        k += 1
    return None if dry else DENY


def _check_git_worktree(words):
    """git worktree remove -f or --force deletes a worktree that holds untracked or modified files: deny.
    An expansion before -- may become -f: deny (cannot parse)."""
    if not words:
        return None
    if words[0].opaque:
        return _uncertain_scan(words)
    if words[0].text != "remove":
        return None
    for word in words[1:]:
        v = word.text
        if word.opaque:
            return CANNOT_PARSE
        if v == "--":
            break
        if v.startswith("--"):
            name = v.partition("=")[0]
            if len(name) > 2 and "--force".startswith(name):
                return DENY
        elif v.startswith("-") and "f" in v[1:]:
            return DENY
    return None


def _check_git_reset(words):
    """git reset --hard (or an abbreviation such as --har) overwrites modified tracked files: deny."""
    for word in words:
        v = word.text
        if v == "--":
            break
        name = v.partition("=")[0]
        if v.startswith("--") and len(name) > 2 and "--hard".startswith(name):
            return DENY
    return None


def _check_git_abandon(words, longs):
    """Round 31 (qanorm30 MINOR-1): git rebase --abort or --skip and git am --abort (round 37: also git
    merge --abort and git cherry-pick --abort; round 38: also git am --skip, git cherry-pick --skip and
    git revert --abort or --skip, the whole set derived at GIT_ABANDON_OPTIONS) reset working-tree
    files to a commit, so they can throw away local changes to tracked files as git reset --hard does
    (inference from git's documentation, not witnessed): deny when a word before -- is one of longs or
    abbreviates one. As for git reset --hard, an expansion is not read (see RESIDUAL)."""
    for word in words:
        v = word.text
        if v == "--":
            break
        name = v.partition("=")[0]
        if v.startswith("--") and len(name) > 2 and any(option.startswith(name) for option in longs):
            return DENY
    return None


def _check_git_stash(words):
    """git stash (push or save, or no subcommand) with -u, --include-untracked, -a or --all stashes the
    untracked (with -a also ignored) files and deletes them from the working tree: deny."""
    k = 0
    if words and not words[0].opaque and not words[0].text.startswith("-"):
        if words[0].text not in ("push", "save"):
            return None  # list, show, pop, apply and the like
        k = 1
    while k < len(words):
        word = words[k]
        v = word.text
        if v == "--":
            break
        if word.opaque:
            k += 1
            continue
        if v.startswith("--"):
            name, eq, _value = v.partition("=")
            if len(name) > 2 and ("--include-untracked".startswith(name) or "--all".startswith(name)):
                return DENY
            takes_value = name == "--pathspec-from-file" or (len(name) > 2 and "--message".startswith(name))
            if takes_value and not eq:
                k += 1  # its value
        elif v.startswith("-") and len(v) > 1:
            for idx, c in enumerate(v[1:]):
                if c == "m":
                    if not v[idx + 2:]:
                        k += 1  # -m MESSAGE
                    break
                if c in "ua":
                    return DENY
        k += 1
    return None


def _git_not_a_ref(text):
    """A word that git check-ref-format rejects as a branch name (., a leading . or /, a trailing /, /. or
    //, and round 17 (qanorm16 F3): *, ? or [, which git reads as a pathspec glob), so that git checkout
    reads it as a path."""
    # Round 18 (qanorm17 m5): also pathspec magic (a leading :, as in :(top) or :/) and a leading ~ (bash
    # expands it to a home directory path; ~ is never in a branch name)
    return (text.startswith((".", "/", ":", "~")) or text.endswith("/") or "/." in text or "//" in text
            or any(c in text for c in "*?["))


def _check_git_checkout(words):
    """git checkout -f or --force of a path (one named after --, --pathspec-from-file, a second operand
    after the tree-ish, an operand that cannot be a branch name, such as ., or round 17 (qanorm16 F3) an
    operand built at run time, such as a glob or "$F", which may be or become a path or several) overwrites
    it: deny. A single literal operand that may be a branch or a path (git checkout -f WORD) is a
    residual. Round 39 (qanorm38 F1): -m, --merge, --conflict, --ours, --theirs, -2 and -3
    (GIT_STAGE_REWRITE_OPTIONS) each rewrite a conflicted path from the index stages: deny with any
    operand, or a path named as above (git checkout -m WORD included, as WORD may be a path). Round 40
    (qanorm39 F1): every long option is read by _git_long_names, so --pathspec-fr= and the other
    abbreviations git accepts name a path as the full option does; (qanorm39 F3) a first operand that
    is an operation ref (_GIT_OPERATION_REF, git checkout MERGE_HEAD -- f) with a path named: deny;
    (qanorm39 F4) -U takes the rest of its cluster or the next word as its value. Round 41 (qanorm40 N4):
    an operation ref as any operand before --, not only the first (git checkout $OPT MERGE_HEAD -- f);
    (qanorm40 N7) every word after --end-of-options is an operand, as git's parse-options reads it
    (inference from git's documentation, not witnessed), with -- still ending the tree-ish operands."""
    force = False
    stage = False
    paths = False
    operation_tree = False
    operands = 0
    end_of_options = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if v == "--":
            paths = paths or k + 1 < len(words)
            break
        if word.opaque:
            operands += 1
            paths = True
            k += 1
            continue
        if v == "--end-of-options" and not end_of_options:
            end_of_options = True
        elif end_of_options:
            operation_tree = operation_tree or bool(_GIT_OPERATION_REF.match(v))
            operands += 1
            paths = paths or _git_not_a_ref(v) or v.startswith("-")
        elif v.startswith("--"):
            name, eq, _value = v.partition("=")
            longs = _git_long_names(name, "checkout")
            if "--force" in longs:
                force = True
            if longs & {"--theirs", "--ours", "--pathspec-from-file"}:
                paths = True  # round 20 (qanorm19 MINOR-3): with --theirs or --ours each operand is a path
            if longs & set(GIT_STAGE_REWRITE_OPTIONS["checkout"]):
                stage = True  # round 39 (qanorm38 F1)
            if not eq and longs & GIT_PATH_VALUE_LONGS:
                k += 1  # round 16: its value is not an operand
        elif v.startswith("-") and len(v) > 1:
            for idx, c in enumerate(v[1:]):
                if c in "bBU":
                    if not v[idx + 2:]:
                        k += 1  # -b BRANCH, -U N (round 40, qanorm39 F4)
                    break
                if c == "f":
                    force = True
                if c in "23":
                    paths = True  # round 20: -2 is --ours and -3 is --theirs
                if c in "m23":
                    stage = True  # round 39 (qanorm38 F1)
        else:
            # Round 16 (qanorm15 MN3): git checkout [-f] TREE-ISH PATH..., and a path that is no branch;
            # round 41 (qanorm40 N4): an operation ref in any operand position (an expansion before it may
            # become no word or an option)
            operation_tree = operation_tree or bool(_GIT_OPERATION_REF.match(v))
            operands += 1
            paths = paths or _git_not_a_ref(v)
        k += 1
    # Round 18 (qanorm17 MD2): git checkout -f with no operand discards every local change to tracked files
    if force and (paths or operands != 1):
        return DENY
    # Round 40 (qanorm39 F3): git checkout MERGE_HEAD -- f (or MERGE_HEAD f) writes another version than
    # the hand resolution (stage 3's, or for REVERT_HEAD the base's; round 41, qanorm40 N2)
    if operation_tree and (paths or operands > 1):
        return DENY
    # Round 39 (qanorm38 F1): a stage-rewrite option with any operand. git checkout -m WORD is denied too,
    # since WORD may be a conflicted path (git checkout -m f, --merge f and --conflict=diff3 f recreated the
    # conflict, witnessed); that over-denies a branch switch, for which git switch -m BRANCH stays allowed
    return DENY if stage and (paths or operands > 0) else None


def _git_long_names(name, command):
    """Round 40 (qanorm39 F1): the long options of git command (GIT_PATH_COMMAND_LONGS) that name, the part
    of a word before =, stands for as git's parse-options reads it: the option it equals, or else every
    option it is a prefix of (one when git accepts it as an abbreviation; several when git refuses it as
    ambiguous, read as all of them in the safe direction). An empty set for -- alone or a short option."""
    if len(name) < 3 or not name.startswith("--"):
        return frozenset()
    longs = GIT_PATH_COMMAND_LONGS[command]
    if name in longs:
        return frozenset((name,))
    return frozenset(option for option in longs if option.startswith(name))


def _check_git_restore(words):
    """Round 39 (qanorm38 F1): git restore with -m, --merge, --conflict, --ours, --theirs, -2 or -3
    (GIT_STAGE_REWRITE_OPTIONS) rewrites each named conflicted path from the index stages, overwriting a
    hand resolution (witnessed, git 2.53.0): deny when a path is named (an operand, a word after --,
    --pathspec-from-file, or an expansion, which may be or become a path). git restore has no branch form,
    so every operand is a path; with no path git refuses to run (witnessed). The values of -s, --source,
    -U, --unified, --inter-hunk-context and --conflict are not paths. As for git checkout -f, an expansion
    that may become one of these options is not read (see RESIDUAL). Round 40 (qanorm39 F1): every long
    option is read by _git_long_names, shared with git checkout; (qanorm39 F3) a source that is an
    operation ref (_GIT_OPERATION_REF, git restore --source=MERGE_HEAD f) with a path named: deny. Round
    41 (qanorm40 N7): every word after --end-of-options is a path, as git's parse-options reads it
    (inference from git's documentation, not witnessed)."""
    stage = False
    paths = False
    sources = []
    end_of_options = False
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if v == "--":
            paths = paths or k + 1 < len(words)
            break
        if word.opaque:
            paths = True
            k += 1
            continue
        if v == "--end-of-options" and not end_of_options:
            end_of_options = True
        elif end_of_options:
            paths = True
        elif v.startswith("--"):
            name, eq, value = v.partition("=")
            longs = _git_long_names(name, "restore")
            if longs & set(GIT_STAGE_REWRITE_OPTIONS["restore"]):
                stage = True
            if "--pathspec-from-file" in longs:
                paths = True
            if "--source" in longs:
                sources.append(value if eq else (words[k + 1].text if k + 1 < len(words) else ""))
            if not eq and longs & GIT_PATH_VALUE_LONGS:
                k += 1  # its value
        elif v.startswith("-") and len(v) > 1:
            for idx, c in enumerate(v[1:]):
                if c in "sU":
                    if not v[idx + 2:]:
                        k += 1  # -s TREE, -U N
                    if c == "s":
                        sources.append(v[idx + 2:] or (words[k].text if k < len(words) else ""))
                    break
                if c in "m23":
                    stage = True
        else:
            paths = True
        k += 1
    operation_tree = any(_GIT_OPERATION_REF.match(source) for source in sources)
    return DENY if (stage or operation_tree) and paths else None


def _check_git_switch(words):
    """git switch -f, --force or --discard-changes throws away local changes to tracked files: deny. -c
    and -C take the rest of their cluster as the branch name."""
    for word in words:
        v = word.text
        if v == "--":
            break
        if word.opaque:
            continue
        if v.startswith("--"):
            name = v.partition("=")[0]
            if len(name) > 2 and ("--force".startswith(name) or "--discard-changes".startswith(name)):
                return DENY
        elif v.startswith("-") and len(v) > 1:
            for c in v[1:]:
                if c in "cC":
                    break
                if c == "f":
                    return DENY
    return None


def _check_git_run(words, depth):
    """A command git runs from words (git submodule foreach COMMAND..., git bisect run COMMAND...): git
    gives one word to the shell as a command string, and with several the shell reads the first word, so
    check the first word as a command string and all of them as a command."""
    if not words:
        return None
    first = _check_command_word(words[:1], depth)
    if first == DENY:
        return DENY
    whole = _check_argv(words, depth + 1) if len(words) > 1 else None
    if whole == DENY:
        return DENY
    return first or whole


def _check_git_submodule(words, depth):
    """git submodule [--quiet] [--cached] foreach [--recursive] [--quiet] COMMAND runs COMMAND in each
    submodule: check it."""
    k = 0
    while k < len(words) and not words[k].opaque and words[k].text in ("-q", "--quiet", "--cached"):
        k += 1
    if k >= len(words):
        return None
    if words[k].opaque:
        return _uncertain_scan(words[k:]) or _form_scan(words[k:])  # a subcommand built at run time
    if words[k].text in ("deinit", "update"):
        # Round 18 (qanorm17 MD2): git submodule deinit -f or --force removes a submodule's working tree
        # even when it holds local changes; an expansion before -- may become -f (cannot parse).
        # Round 30 (qanorm29 F1): git submodule update -f or --force (with or without --checkout) throws
        # away local changes in submodule working trees (inference from git's documentation, not
        # witnessed), so it is read the same way
        return _git_force_option(words[k + 1:], "f", ("--force",))
    if words[k].text != "foreach":
        return None
    k += 1
    while k < len(words) and not words[k].opaque and words[k].text in ("--recursive", "-q", "--quiet"):
        k += 1
    if k < len(words) and words[k].text == "--":
        k += 1
    return _check_git_run(words[k:], depth)


def _git_force_option(words, letters, longs):
    """Round 18 (qanorm17 MD2): deny when a word before -- is a short cluster holding one of letters or a
    long option that is or abbreviates one of longs; an expansion there may become one (cannot parse)."""
    unsure = False
    for word in words:
        v = word.text
        if v == "--":
            break
        if word.opaque:
            unsure = True
            continue
        if v.startswith("--"):
            name = v.partition("=")[0]
            if len(name) > 2 and any(option.startswith(name) for option in longs):
                return DENY
        elif v.startswith("-") and any(c in letters for c in v[1:]):
            return DENY
    return CANNOT_PARSE if unsure else None


def _check_git_read_tree(words):
    """Round 18 (qanorm17 MD2): git read-tree -u --reset overwrites the working tree with the tree it reads,
    discarding local changes: deny when both are given. An expansion before -- may become either."""
    update = reset = unsure = False
    for word in words:
        v = word.text
        if v == "--":
            break
        if word.opaque:
            unsure = True
        elif v.startswith("--"):
            name = v.partition("=")[0]
            reset = reset or (len(name) > 4 and "--reset".startswith(name))
        elif v.startswith("-"):
            update = update or "u" in v[1:]
    if update and reset:
        return DENY
    return CANNOT_PARSE if unsure and (update or reset) else None


def _check_git_bisect(words, depth):
    """git bisect run COMMAND [ARG]... runs COMMAND at each step: check it."""
    if not words:
        return None
    if words[0].opaque:
        return _uncertain_scan(words) or _form_scan(words)  # a subcommand built at run time
    if words[0].text != "run":
        return None
    return _check_git_run(words[1:], depth)


def _git_long_match(name, options):
    """The long option that name is, or abbreviates (git accepts an unambiguous prefix)."""
    if name in options:
        return name
    if len(name) > 2:
        for option in options:
            if option.startswith(name):
                return option
    return None


def _check_git_command_options(table, words, depth):
    """A git subcommand option whose value git runs as a command (git rebase --exec or -x, git difftool
    --extcmd, git filter-branch --tree-filter and the like, --upload-pack, --receive-pack, the send-email
    --*-cmd options, git grep -O): check each such value as a shell command string."""
    long_value, long_attached, short_value, short_attached, short_other = table
    result = None
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if v == "--":
            break
        step = 1
        command = None
        if word.opaque or not v.startswith("-") or v == "-":
            pass
        elif v.startswith("--"):
            name, eq, value = v.partition("=")
            option = _git_long_match(name, long_value + long_attached)
            if option in long_value or (option in long_attached and eq):
                if eq:
                    command = Word(value, word.raw, word.quoted, word.opaque)
                elif k + 1 < len(words):
                    command = words[k + 1]
                    step = 2
        else:
            cluster = v[1:]
            for idx, c in enumerate(cluster):
                value = cluster[idx + 1:]
                if c in short_value or (c in short_attached and value):
                    if value:
                        command = Word(value, word.raw, word.quoted, word.opaque)
                    elif k + 1 < len(words):
                        command = words[k + 1]
                        step = 2
                    break
                if c in short_attached:
                    break
                if c in short_other:
                    if not value:
                        step = 2  # its value is the next word
                    break
        if command is not None:
            got = _check_command_word([command], depth)
            if got == DENY:
                return DENY
            result = result or got
        k += step
    return result


def _check_trap(words, depth):
    """trap ACTION SIGNAL...: the shell later runs ACTION as a command string, so check it as one."""
    k = 0
    if k < len(words) and words[k].text == "--":
        k += 1
    if k >= len(words):
        return None
    action = words[k].text
    if k == 0 and action.startswith("-") and action != "-":
        if action in ("-l", "-p", "-P", "-lp", "-pl"):
            return None  # it only lists or prints traps
        return _uncertain_scan(words)
    if action == "-":
        return None  # it resets the signals
    return _check_command_text(action, depth + 1)


# Round 18 (qanorm17 MD1): IPython long options that take no value; any other long option without = may
# take the next word as its value.
_IPY_LONG_FLAGS = frozenset((
    "--help", "--help-all", "--version", "--debug", "--quiet", "--init", "--autoindent", "--no-autoindent",
    "--automagic", "--no-automagic", "--pdb", "--no-pdb", "--pprint", "--no-pprint", "--color-info",
    "--no-color-info", "--ignore-cwd", "--no-ignore-cwd", "--nosep", "--autoedit-syntax",
    "--no-autoedit-syntax", "--simple-prompt", "--no-simple-prompt", "--banner", "--no-banner",
    "--confirm-exit", "--no-confirm-exit", "--term-title", "--no-term-title", "--classic", "--quick"))


def _check_eval(words, depth):
    """Round 18 (qanorm17 m1): eval joins its words with spaces and runs the result as a command, as trap
    runs its action: check it as a command string (a round 15 removal form in a string it cannot parse
    counts as for a shell -c string). An expansion makes the string unknown: deny (cannot parse) when the
    words hold a removal word or form."""
    if words and words[0].text == "--":
        words = words[1:]
    if not words:
        return None
    result = _check_command_text(" ".join(w.text for w in words), depth + 1, True)
    if result == DENY:
        return DENY
    if any(w.opaque for w in words):
        return _uncertain_scan(words) or _form_scan(words) or result
    return result


def _combined(result, got):
    """Round 20: a later verdict joined to an earlier one (a deny wins, then cannot-parse)."""
    return DENY if got == DENY else (result or got)


def _check_python(words, depth=0, ipython=False):
    result = None  # round 20: what an ipython config option that runs code found before this word
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return _uncertain_scan(words[k:]) or result
        if v in ("-", "--"):
            return result
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            if ipython and name == "--c":
                # Round 19 (qanorm18 MEDIUM-3): traitlets also reads the one-letter -c alias with two
                # dashes (--c PROGRAM, --c=PROGRAM); that it does is inference from its documentation
                if eq:
                    return _combined(result, _check_python_program(value, words[k + 1:], depth, ipython))
                if k + 1 >= len(words):
                    return result
                return _combined(result, _check_python_program(words[k + 1].text, words[k + 2:], depth,
                                                               ipython))
            if ipython and name.rpartition(".")[2] in ("code_to_run", "exec_lines"):
                # Round 20 (qanorm19 MINOR-2): the config options --InteractiveShellApp.code_to_run (also
                # --TerminalIPythonApp. and any other class prefix) and .exec_lines run their value as
                # code: a program, or a list of program lines. That IPython reads them so is inference
                # from the IPython and traitlets documentation, not witnessed.
                if eq:
                    target = Word(value, word.raw, word.quoted, word.opaque)
                    step = 1
                elif k + 1 < len(words):
                    target = words[k + 1]
                    step = 2
                else:
                    return result
                got = _check_ipython_config_code(target, words[k + step:], depth)
                if got == DENY:
                    return DENY
                result = result or got
                k += step
                continue
            if ipython and not eq and name not in _IPY_LONG_FLAGS:
                # Round 18 (qanorm17 MD1): IPython (traitlets) also takes an option value as the next
                # word (--profile foo, --log-level 10); read a next word that is no option as that value
                k += 2 if k + 1 < len(words) and not words[k + 1].text.startswith("-") else 1
                continue
            k += 2 if (name == "--check-hash-based-pycs" and not eq) else 1
            continue
        if v.startswith("-") and len(v) > 1:
            cluster = v[1:]
            step = 1
            for idx, c in enumerate(cluster):
                if c == "c":
                    program = cluster[idx + 1:]
                    later = words[k + 1:]
                    if not program:
                        if k + 1 >= len(words):
                            return result
                        program = words[k + 1].text
                        later = words[k + 2:]
                    return _combined(result, _check_python_program(program, later, depth, ipython))
                if c == "m":
                    return result
                if c in "WX":
                    if not cluster[idx + 1:]:
                        step = 2
                    break
            k += step
            continue
        return result  # a script file: residual
    return result


def _check_ipython_config_code(target, later, depth):
    """Round 20 (qanorm19 MINOR-2): the value of an ipython code_to_run or exec_lines option: a python
    literal list or tuple of strings is checked line by line, and the value itself as a program too. An
    expansion: deny (cannot parse) when it holds a removal word or form."""
    if target.opaque:
        return _uncertain_scan([target]) or _form_scan([target])
    programs = [target.text]
    try:
        value = ast.literal_eval(target.text)
    except (SyntaxError, ValueError, TypeError, MemoryError, RecursionError):
        value = None
    if isinstance(value, (list, tuple)):
        programs.extend(item for item in value if isinstance(item, str))
    elif isinstance(value, str):
        programs.append(value)
    result = None
    for program in programs:
        got = _check_python_program(program, later, depth, True)
        if got == DENY:
            return DENY
        result = result or got
    return result


def _check_python_program(program, later, depth, ipython):
    result = _check_python_source(program, depth, ipython)
    if result == DENY:
        return DENY
    # Round 18 (qanorm17 MD3): a program that runs sys.argv runs the later words
    return _passed_arguments(_PY_ARGS, program, later, depth) or result


def _ipython_shell_strings(source):
    """Round 17 (qanorm16 F1): the shell command strings of an IPython program: the rest of a ! or !! line
    (also NAME = !cmd) and of a %sx or %system line, and, for a %%bash, %%sh, %%script, %%sx, %%system or
    %%! line, the rest of that line (the %%script program) and every later line (the cell body)."""
    strings = []
    lines = source.split("\n")
    for idx, line in enumerate(lines):
        match = _IPY_ESCAPE_LINE.match(line)
        if match is None:
            continue
        strings.append(match.group(4))
        if match.group(3):
            strings.append("\n".join(lines[idx + 1:]))
    return strings


# Round 18 (qanorm17 m4): a line that IPython reads as its default rm or rmdir shell alias (automagic,
# also written %rm), not as a python assignment
_IPY_ALIAS_LINE = re.compile(r"[ \t]*%?((?:rm|rmdir)(?:[ \t]+(?!=(?!=)).*)?)\Z")


def _ipython_alias_lines(source):
    return [m.group(1) for m in map(_IPY_ALIAS_LINE.match, source.split("\n")) if m]


def _check_python_source(source, depth=0, ipython=False):
    if ipython:
        result = None
        for string in _ipython_alias_lines(source):
            got = _check_command_text(string, depth + 1, True)
            if got == DENY:
                return DENY
            result = result or got
        if result is not None:
            return result
    try:
        tree = ast.parse(source, mode="exec")
    except (SyntaxError, ValueError):
        if ipython:
            # Round 17 (qanorm16 F1): IPython runs a ! line and the shell magics through the shell, so
            # check each such string as a shell command string
            result = None
            for string in _ipython_shell_strings(source):
                got = _check_command_text(string, depth + 1, True)
                if got == DENY:
                    return DENY
                result = result or got
            if result is not None:
                return result
        # round 14 (qanorm13 F3); round 16 (qanorm15 M2): also a shell call with a round 15 removal form;
        # round 17 (qanorm16 F1): an IPython program with a round 15 removal form in its text
        removes = _has_removal_text(source) or ((ipython or _PY_SHELL_CALL.search(source))
                                                and _has_removal_form_text(source))
        return CANNOT_PARSE if removes else None
    if _py_tree_removes(tree):
        return DENY
    # Round 15: a program that names subprocess, system or popen (a shell command run through
    # subprocess, os.system or os.popen) and holds a removal word anywhere; round 16 (qanorm15 M2): or a
    # round 15 removal form (git clean, git reset --hard, cargo clean and the like); round 17 (qanorm16
    # F1): for IPython, also a program that names get_ipython (its system, getoutput and magic calls)
    shell_call = _IPY_SHELL_CALL if ipython else _PY_SHELL_CALL
    import unicodedata
    for text in (source, unicodedata.normalize("NFKC", source)):
        if shell_call.search(text) and (_REMOVAL_TEXT.search(text) or _has_removal_form_text(text)):
            return DENY
    return None


def _py_literal_index(node):
    """The integer a subscript slice holds when it is an integer literal (0, 1, -1), else None."""
    sign = 1
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        sign = -1 if isinstance(node.op, ast.USub) else 1
        node = node.operand
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return sign * int(node.value)
    return None


def _py_is_os_ref(node, os_names):
    if isinstance(node, ast.Name):
        return node.id in os_names
    # Round 24 (qanorm23 F1): an os module reached through an expression: a walrus ((o := os).remove),
    # either branch of a conditional expression ((os if c else x).remove), and a tuple or list element
    # indexed by an integer literal ((os,)[0].remove, [x, os][-1].remove)
    if isinstance(node, ast.NamedExpr):
        return _py_is_os_ref(node.value, os_names)
    if isinstance(node, ast.IfExp):
        return _py_is_os_ref(node.body, os_names) or _py_is_os_ref(node.orelse, os_names)
    # Round 25 (qanorm24 MINOR 1): any operand of or and and ((os or 0).remove, (1 and os).remove,
    # o = os or None), as for either branch of a conditional expression
    if isinstance(node, ast.BoolOp):
        return any(_py_is_os_ref(value, os_names) for value in node.values)
    if isinstance(node, ast.Subscript) and isinstance(node.value, (ast.Tuple, ast.List)):
        index = _py_literal_index(node.slice)
        elts = node.value.elts
        if index is None:
            return False
        if any(isinstance(elt, ast.Starred) for elt in elts):
            # positions after a starred element are not known: any element that is an os module counts
            return any(_py_is_os_ref(elt, os_names) for elt in elts if not isinstance(elt, ast.Starred))
        if -len(elts) <= index < len(elts):
            return _py_is_os_ref(elts[index], os_names)
        return False
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Name) and func.id == "__import__":
            return True
        if isinstance(func, ast.Attribute) and func.attr == "import_module":
            return True
    return False


def _py_bound_pairs(target, value):
    """The (name, value) pairs an assignment binds to plain names, also pairwise through a tuple or list
    target with a tuple or list value of the same length (o, p = os, 1)."""
    if isinstance(target, ast.Name):
        return [(target.id, value)]
    if (isinstance(target, (ast.Tuple, ast.List)) and isinstance(value, (ast.Tuple, ast.List))
            and len(target.elts) == len(value.elts)):
        pairs = []
        for sub_target, sub_value in zip(target.elts, value.elts):
            pairs.extend(_py_bound_pairs(sub_target, sub_value))
        return pairs
    return []


def _py_tree_removes(tree):
    os_names = set(PY_OS_MODULES)
    star = False
    # Round 23 (qanorm22 F2): a name bound to an os module (o = os, o = __import__('os'), (o := os), and
    # a chain of such names) counts as an os module, so o.remove and getattr(o, "remove") deny. shutil and
    # pathlib need no tracking: their removal attributes (rmtree, unlink, rmdir) deny on any object.
    bindings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                bindings.extend(_py_bound_pairs(target, node.value))
        elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)) and node.value is not None:
            bindings.extend(_py_bound_pairs(node.target, node.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if alias.asname:
                    if alias.name in PY_OS_MODULES:
                        os_names.add(alias.asname)
                elif root in PY_OS_MODULES:
                    os_names.add(root)
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in PY_FROM_MODULES:
                for alias in node.names:
                    if alias.name == "*":
                        star = True
                    elif alias.name in PY_REMOVE_NAMES:
                        return True
    changed = True
    while changed:
        changed = False
        for name, value in bindings:
            if name not in os_names and _py_is_os_ref(value, os_names):
                os_names.add(name)
                changed = True
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr in PY_ALWAYS_REMOVE_ATTRS:
                return True
            if node.attr == "remove" and _py_is_os_ref(node.value, os_names):
                return True
        elif isinstance(node, ast.Name):
            if star and node.id in PY_REMOVE_NAMES:
                return True
        elif isinstance(node, ast.Call):
            func = node.func
            if (isinstance(func, ast.Name) and func.id == "getattr" and len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant) and node.args[1].value in PY_REMOVE_NAMES):
                # getattr(X, "remove") is judged as X.remove is: only an os module's remove removes
                if node.args[1].value != "remove" or _py_is_os_ref(node.args[0], os_names):
                    return True
            # Round 25 (qanorm24 MINOR 2): methodcaller with a literal removal name is judged as getattr
            # with that name is: another removal name denies wherever it is, and "remove" denies when the
            # caller is applied at once to an os module (operator.methodcaller("remove", "x")(os))
            name = _py_methodcaller_name(node)
            if name is not None and name != "remove":
                return True
            if (_py_methodcaller_name(func) == "remove" and node.args
                    and _py_is_os_ref(node.args[0], os_names)):
                return True
    return False


def _py_methodcaller_name(node):
    """The literal removal name of a methodcaller(NAME, ...) call (operator.methodcaller or a from-import
    of it), or None."""
    if not isinstance(node, ast.Call) or not node.args:
        return None
    func = node.func
    if not ((isinstance(func, ast.Name) and func.id == "methodcaller")
            or (isinstance(func, ast.Attribute) and func.attr == "methodcaller")):
        return None
    first = node.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str) and first.value in PY_REMOVE_NAMES:
        return first.value
    return None


# --- decisions ---------------------------------------------------------------------------------------

def _deobfuscated(text):
    """The raw text with $'...' decoded (cut at a NUL, as bash does), the $ of $"..." dropped, and
    quotes, backslashes, NULs and line continuations removed."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("$'", i):
            try:
                decoded, i = _ansi_c(text, i + 2)
            except ParseError:
                # Round 14 (qanorm13 F2): skip a $' it cannot decode and keep decoding the rest
                i += 2
                continue
            out.append(decoded)
            continue
        if text.startswith("\\\n", i):
            i += 2
            continue
        if text.startswith('$"', i):
            i += 1
            continue
        if text[i] not in "\\'\"\x00":
            out.append(text[i])
        i += 1
    return "".join(out)


def _ansi_c_holds_nul(text):
    """Whether any $'...' in the raw text decodes to a NUL (bash cuts the string there)."""
    i = text.find("$'")
    while i >= 0:
        try:
            decoded, _end = _ansi_c(text, i + 2, keep_nul=True)
        except ParseError:
            decoded = ""
        if "\x00" in decoded:
            return True
        i = text.find("$'", i + 1)  # every $', even one inside quotes: the safe direction
    return False


def _unreadable_constructs(ctx, command, argvs):
    """Constructs in the command that the lexer cannot read exactly (see FAIL-SAFE in the docstring)."""
    found = set(ctx.unreadable)
    if _CONTINUATION_IN_WORD.search(command):
        found.add("a line continuation inside a word")
    if "\\\n" in command and _HEREDOC_OP.search(command):
        found.add("a line continuation in a command with a here-document")
    if _ansi_c_holds_nul(command):
        found.add("a NUL from $'...' decoding")
    for argv in argvs:
        j = 0
        while j < len(argv) and _is_assignment(argv[j].raw):
            j += 1
        if j < len(argv) and _SUBSCRIPT_WORD.match(argv[j].raw):
            found.add("a NAME[ command word (a subscript it does not read)")
        if any(_basename(word.text) in _EVAL_LIKE for word in argv):
            found.add("alias, hash, mapfile or readarray")
        if any(word.text in _STRING_EVAL for word in argv):
            found.add("a string-evaluation builtin")
        for k, word in enumerate(argv):
            if _basename(word.text) == "env" and any(_ENV_SPLIT_OPTION.match(w.text) for w in argv[k + 1:]):
                found.add("env -S")
    if _BRACE_COMMAND_SUB.search(command):
        found.add("a ${ } or ${| } command substitution")
    if _DOLLAR_QUOTE.search(command):
        found.add("a dollar-quote")
    if _HASH_ALIAS_ARRAYS.search(command):
        found.add("BASH_CMDS or BASH_ALIASES")
    return found


_PY_GETATTR = re.compile(r"(?<![A-Za-z0-9_])getattr(?![A-Za-z0-9_])")
_STRIP_QUOTING = re.compile(r"[\\'\"\x00]")


def _has_removal_text(text):
    # python normalizes identifiers with NFKC, and getattr takes a name that ast may fold from
    # escapes or adjacent literals, so the python check can match with no removal word in the text
    import unicodedata
    folded = unicodedata.normalize("NFKC", text)
    # Round 14 (qanorm13 F2): also with every quote and backslash removed and no $'...' decoding, for a
    # $' that bash does not read as a dollar-quote ("$'" in double quotes)
    return bool(_REMOVAL_TEXT.search(text) or _REMOVAL_TEXT.search(_deobfuscated(text))
                or _REMOVAL_TEXT.search(folded) or _REMOVAL_TEXT.search(_deobfuscated(folded))
                or _REMOVAL_TEXT.search(_STRIP_QUOTING.sub("", text.replace("\\\n", "")))
                or _REMOVAL_TEXT.search(_STRIP_QUOTING.sub("", folded.replace("\\\n", "")))
                or _PY_GETATTR.search(text))


# Round 18 (qanorm17 M2): a shell, at, batch or a known interpreter that reads its program from stdin or
# from a process-substitution file. Round 19 (qanorm18 MAJOR-1, MAJOR-2, MEDIUM-2): structural. A reader
# counts wherever it is in the command, and its standard input counts as fed by the command when the
# command holds anything that feeds a standard input or a file descriptor: a pipe (on one line or
# continued onto the next), an input redirection, a here-document or here-string, an input
# file-descriptor duplication, a process substitution or coproc. Round 18 split the command into
# pipelines and ended one at a newline right after |, which bash continues; that split is gone.
_FEED_OPS = frozenset(("|", "|&", "<", "<>", "<<", "<<-", "<<<", "<&"))
_STDIN_PATH = re.compile(r"(?:/dev/stdin|/dev/fd/[0-9]+|/proc/[^/]+/fd/[0-9]+)\Z")
_SOURCE_NAMES = frozenset(("source", "."))
_READER_SPLIT = re.compile(r"[\s;&|()<>`'\"{}]+")


def _inner_command(words):
    """The argv that a run of leading assignments and wrappers (WRAPPERS) runs, or None when an option or
    construct leaves it unknown."""
    for _level in range(MAX_CHECK_DEPTH + 1):
        j = 0
        while j < len(words) and _is_assignment(words[j].raw):
            j += 1
        words = words[j:]
        if not words or words[0].opaque:
            return words
        name = _basename(words[0].text)
        spec = WRAPPERS.get(name)
        if spec is None:
            return words
        rest = words[1:]
        j, ok, seen, split = _parse_options(spec, rest)
        if not ok or split is not None or name == "flock":
            return None
        if name == "command" and seen & {"v", "V"}:
            return []
        if name in ("env", "sudo"):
            while j < len(rest) and "=" in rest[j].text and not rest[j].text.startswith("="):
                j += 1
        if name in ("timeout", "taskset"):
            j += 1
        if name == "chrt" and j < len(rest) and rest[j].text.isdigit():
            j += 1
        # Round 20 (qanorm19 MAJOR-1): sudo -s, sudo -i (--shell, --login) and doas -s with no command
        # start a shell, which reads its commands from standard input
        if (j >= len(rest) and name in ("sudo", "doas")
                and ("s" in seen or (name == "sudo" and ("i" in seen or any(
                    _long_matches(w.text.partition("=")[0], ("--shell", "--login")) for w in rest[:j]))))):
            return [Word.literal("sh")]
        words = rest[j:]
    return None


def _is_program_reader(name):
    # Round 20 (qanorm19 MAJOR-1, MINOR-1): su (which starts a shell) and ssh (a remote shell) too
    return (name in SHELL_NAMES or name in ("at", "batch", "source", "su", "ssh")
            or bool(_PYTHON_NAME.match(name)) or bool(_PERL_NAME.match(name)))


def _su_source(words, depth):
    """Round 20 (qanorm19 MAJOR-1): su [OPTIONS] [-] [USER [ARG]...] with no -c, --command or
    --session-command starts the user's shell, which reads its commands from standard input; with one,
    that string may itself run a program read from stdin. An expansion counts as reading stdin."""
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return True, None
        step = 1
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            matches = _long_matches(name, _SU_LONG)
            if matches & {"--command", "--session-command"}:
                string = (Word(value, word.raw, word.quoted, word.opaque) if eq
                          else (words[k + 1] if k + 1 < len(words) else None))
                return _string_reads_stdin(string, depth), None
            if matches and matches <= {"--shell", "--group", "--supp-group", "--whitelist-environment"} \
                    and not eq:
                step = 2
        elif v.startswith("-") and len(v) > 1:
            cluster = v[1:]
            for idx, c in enumerate(cluster):
                value = cluster[idx + 1:]
                if c == "c":
                    string = Word(value, value) if value else (words[k + 1] if k + 1 < len(words) else None)
                    return _string_reads_stdin(string, depth), None
                if c in "sgGw":
                    if not value:
                        step = 2
                    break
        k += step
    return True, None


def _names_reader(text):
    """Whether a word of a text it cannot read is a reader name (the safe direction)."""
    return any(_is_program_reader(_basename(piece)) for piece in _READER_SPLIT.split(text) if piece)


def _shell_string_after(words, k):
    """The -c string of a shell whose option cluster is words[k]: the first later word that is no option."""
    j = k + 1 + sum(1 for c in words[k].text[1:] if c in "oO")
    while (j < len(words) and not words[j].opaque and words[j].text[:1] in ("-", "+")
           and words[j].text not in ("-", "--")):
        j += 1 + sum(1 for c in words[j].text[1:] if c in "oO")
    if j < len(words) and not words[j].opaque and words[j].text == "--":
        j += 1
    return words[j] if j < len(words) else None


def _behind_xargs(argv, words):
    """Round 25 (qanorm24 MEDIUM 1): whether xargs is among the wrappers _inner_command looked past in argv
    to reach words. A shell -c with no string operand there takes its string from the input xargs reads
    (echo 'rm -rf x' | xargs -0 sh -c runs sh -c 'rm -rf x'), so it reads its program from stdin."""
    if not words:
        return False
    for idx, word in enumerate(argv):
        if word is words[0]:
            return any(not w.opaque and _basename(w.text) in _XARGS_NAMES for w in argv[:idx])
    return False


def _string_reads_stdin(word, depth):
    """Round 19: whether a shell -c string runs a program read from its standard input, which is the outer
    shell's (sh -c 'cat | sh'). An expansion, a string it cannot parse and the depth cap count as one when
    a reader name is among its words."""
    if word is None:
        return False
    if word.opaque or depth >= MAX_CHECK_DEPTH:
        return word.opaque or _names_reader(word.text)
    ctx = _Ctx()
    try:
        tokens, _end = _lex(ctx, word.text, 0, False)
        argvs = []
        for token_list in [tokens] + ctx.subs:
            argvs.extend(_command_argvs(token_list))
    except ParseError:
        return _names_reader(word.text)
    return any(_reads_program_input(argv, depth + 1) for argv in argvs)


def _program_source(argv, depth=0):
    """For a shell, at, batch, python, perl, source or . argv: (reads its program from stdin, the word
    naming its program file or None). An expansion where an option or the program may be counts as both;
    a shell -c string that itself runs a program read from stdin counts as reading stdin."""
    words = _inner_command(argv)
    if words is None:
        # round 20 (qanorm19 MAJOR-1): behind an option it does not know, sudo or doas may start a shell;
        # round 34 (qanorm33 N4): flock and such a wrapper may run source or . too (flock /tmp/l . <(...))
        return any(_is_program_reader(_basename(w.text)) or _basename(w.text) in ("sudo", "doas")
                   or (_RULES["runner readers"] and w.text in _SOURCE_NAMES)
                   for w in argv if not w.opaque), None
    if not words or words[0].opaque:
        return False, None
    name = _basename(words[0].text)
    if name in _SOURCE_NAMES:
        # Round 19 (qanorm18 MEDIUM-2): source FILE and . FILE run FILE in this shell (bash 5.3: -p PATH)
        k = 1
        while k < len(words) and not words[k].opaque and words[k].text in ("--", "-p"):
            if words[k].text == "--":
                k += 1
                break
            k += 2
        return False, (words[k] if k < len(words) else None)
    if name == "su":
        return _su_source(words[1:], depth)
    if name == "ssh":
        # Round 20 (qanorm19 MINOR-1): ssh's remote shell reads ssh's stdin when it has no command
        ok, seen, command = _ssh_parse(words[1:])
        if not ok:
            return True, None
        if "n" in seen:
            return False, None  # ssh -n reads its standard input from /dev/null
        if command:
            string = Word(" ".join(w.text for w in command), " ".join(w.raw for w in command),
                          any(w.quoted for w in command), any(w.opaque for w in command))
            return _string_reads_stdin(string, depth), None
        return not (seen & _SSH_NO_STDIN_SHELL), None
    if name in _AWK_NAMES or name in ("sed", "gsed"):
        # Round 20 (qanorm19 MINOR-1): awk -f FILE and sed -f FILE read their program from FILE
        files = _awk_programs(words[1:])[1] if name in _AWK_NAMES else _sed_programs(words[1:])[1]
        for target in files:
            if target.opaque or target.text == "-" or _STDIN_PATH.match(target.text):
                return False, target
        return False, (files[0] if files else None)
    if not _is_program_reader(name):
        # Round 34 (qanorm33 N4): uv run, pipx run, poetry run and jobs -x run a later word as a command, so
        # a reader behind them is read as behind a command word it does not know
        runner = _RULES["runner readers"] and (name in RUNNERS or name in ("uv", "jobs"))
        if not _has_rule(name) or runner:
            # Round 20 (qanorm19 MINOR-1): a command word it does not know may be a wrapper (chroot /srv
            # sh, runuser -u bob -- sh): a later unquoted word that names a reader or a wrapper it knows
            # starts an argv that may read stdin; round 34 (qanorm33 N4): or source or .
            for idx in range(1, len(words)):
                word = words[idx]
                piece = _basename(word.text)
                if word.quoted or word.opaque or not (
                        _starts_known_argv(piece) or _is_program_reader(piece)
                        or (_RULES["runner readers"] and word.text in _SOURCE_NAMES)):
                    continue
                if depth >= MAX_CHECK_DEPTH or not _spend_scan_budget():
                    return True, None
                if _reads_program_input(words[idx:], depth + 1):
                    return True, None
        return False, None
    shell = name in SHELL_NAMES
    k = 1
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque:
            return True, word
        if name in ("at", "batch"):
            if v.startswith("-") and len(v) > 1:
                for idx, c in enumerate(v[1:]):
                    if c in "ldrc" and name == "at":
                        return False, None  # it lists, deletes or prints jobs
                    if c in "fqt":
                        value = v[idx + 2:]
                        target = Word.literal(value) if value else (words[k + 1] if k + 1 < len(words) else None)
                        if c == "f":
                            return False, target
                        if not value:
                            k += 1
                        break
                k += 1
                continue
            k += 1  # a time word
            continue
        if v == "--" or v == "-":
            if v == "-":
                return True, None
            k += 1
            break
        if v.startswith("--"):
            option = v.partition("=")[0]
            if shell and name == "fish" and _long_matches(option, _FISH_LONG) & {"--command"}:
                string = (Word(v.partition("=")[2], word.raw, word.quoted, word.opaque) if "=" in v
                          else (words[k + 1] if k + 1 < len(words) else None))
                if string is None and _behind_xargs(argv, words):
                    return True, None  # round 25: xargs passes its input as the string
                return _string_reads_stdin(string, depth), None
            if shell and option in SHELL_VALUE_LONG and "=" not in v:
                if k + 1 < len(words) and words[k + 1].opaque:
                    return True, words[k + 1]  # an rc file it reads as a program
                k += 2
                continue
            k += 2 if option == "--check-hash-based-pycs" and "=" not in v else 1
            continue
        if v[:1] in ("-", "+") and len(v) > 1:
            cluster = v[1:]
            if shell:
                if "c" in cluster:
                    # its program is the -c string; round 19: which may run a program read from stdin
                    string = _shell_string_after(words, k)
                    if string is None and _behind_xargs(argv, words):
                        return True, None  # round 25: xargs passes its input as the string
                    return _string_reads_stdin(string, depth), None
                if "s" in cluster and name != "fish":
                    return True, None
                k += 1 + sum(1 for c in cluster if c in "oO")
                continue
            if _PERL_NAME.match(name) and ("e" in cluster or "E" in cluster):
                return False, None
            if not _PERL_NAME.match(name):
                for idx, c in enumerate(cluster):
                    if c in "cm":
                        return False, None  # python -c PROGRAM or -m MODULE
                    if c in "WX":
                        k += 0 if cluster[idx + 1:] else 1
                        break
            k += 1
            continue
        break
    if name in ("at", "batch"):
        return True, None
    if k >= len(words):
        return True, None
    return False, words[k]


def _reads_program_input(argv, depth=0):
    """Round 19: whether an argv runs a program read from its standard input, or from a file that is a
    process substitution, standard input or a file descriptor (/dev/stdin, /dev/fd/N, /proc/PID/fd/N, -),
    or from an expansion that may be one."""
    stdin, source = _program_source(argv, depth)
    if stdin:
        return True
    return source is not None and (source.opaque or source.text == "-" or bool(_STDIN_PATH.match(source.text)))


def _feeds_input(token_lists):
    """Round 19: whether the command feeds a standard input or a file descriptor from its own text: a pipe,
    an input redirection or duplication, a here-document or here-string, a process substitution or
    coproc, anywhere in it (the safe direction: not only at the reader)."""
    for tokens in token_lists:
        for kind, val in tokens:
            if kind == "op" and val in _FEED_OPS:
                return True
            if kind == "w" and ("<(" in val.raw or ">(" in val.raw or val.raw == "coproc"):
                return True
    return False


# Round 26 (qanorm25 F1): a program that xargs fills from its input. xargs runs its command with the items
# it reads appended, or with -I R, -iR, -i or --replace[=R] put in place of the replace string R ({} for
# -i and --replace), so a command whose program comes from an operand (a shell, su or flock -c or
# --command string, a python or ipython -c program, a perl -e or -E program, an awk or sed program) runs
# the input xargs reads as its program when that operand is missing or holds the replace string.
_XARGS_FLOCK_COMMAND = ("-c", "--command")


def _xargs_replace_strings(words):
    """The replace strings of xargs options words, which _parse_options has read as valid options."""
    spec = WRAPPERS["xargs"]
    found = []
    k = 0
    while k < len(words):
        v = words[k].text
        if v == "--":
            break
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            matches = _long_matches(name, spec.long_args | spec.long_flags)
            if matches == {"--replace"}:
                found.append(value if eq else "{}")
            k += 2 if matches and matches <= spec.long_args and not eq else 1
            continue
        cluster = v[1:]
        step = 1
        for idx, c in enumerate(cluster):
            value = cluster[idx + 1:]
            if c in spec.args:
                if not value:
                    value = words[k + 1].text if k + 1 < len(words) else ""
                    step = 2
                if c == "I":
                    found.append(value)
                break
            if c in spec.optargs:
                if c == "i":
                    found.append(value or "{}")
                break
        k += step
    return found


def _next_operand(words, k, value):
    """The attached value of an option as a word, else words[k + 1] (None when there is none)."""
    if value:
        return Word.literal(value)
    return words[k + 1] if k + 1 < len(words) else None


def _xargs_program_operands(words):
    """For an argv words whose program may come from an operand: the list of its program operands (empty
    when the operand is missing), or None when it takes its program some other way (a script file, -m,
    stdin, awk -f or sed -f) or an expansion leaves that unknown."""
    name = _basename(words[0].text)
    rest = words[1:]
    k = 0
    if name in SHELL_NAMES:
        while k < len(rest):
            word = rest[k]
            v = word.text
            if word.opaque or v in ("-", "--") or v[:1] not in ("-", "+") or len(v) < 2:
                return None
            if v.startswith("--"):
                option, eq, value = v.partition("=")
                if name == "fish" and _long_matches(option, _FISH_LONG) & {"--command"}:
                    string = Word.literal(value) if eq else (rest[k + 1] if k + 1 < len(rest) else None)
                    return [string] if string is not None else []
                k += 2 if option in SHELL_VALUE_LONG and not eq else 1
                continue
            if "c" in v[1:]:
                string = _shell_string_after(words, k + 1)
                return [string] if string is not None else []
            k += 1 + sum(1 for c in v[1:] if c in "oO")
        return None
    if name == "su":
        while k < len(rest):
            word = rest[k]
            v = word.text
            if word.opaque:
                return None
            step = 1
            if v.startswith("--"):
                option, eq, value = v.partition("=")
                matches = _long_matches(option, _SU_LONG)
                if matches & {"--command", "--session-command"}:
                    string = Word.literal(value) if eq else (rest[k + 1] if k + 1 < len(rest) else None)
                    return [string] if string is not None else []
                if matches and matches <= {"--shell", "--group", "--supp-group", "--whitelist-environment"} \
                        and not eq:
                    step = 2
            elif v.startswith("-") and len(v) > 1:
                cluster = v[1:]
                for idx, c in enumerate(cluster):
                    if c == "c":
                        string = _next_operand(rest, k, cluster[idx + 1:])
                        return [string] if string is not None else []
                    if c in "sgGw":
                        if not cluster[idx + 1:]:
                            step = 2
                        break
            k += step
        return None
    if name == "flock":
        # flock [OPTIONS] FILE -c COMMAND (util-linux reads -c or --command right after FILE)
        j, ok, _seen, _split = _parse_options(WRAPPERS["flock"], rest)
        if not ok or j + 1 >= len(rest) or rest[j + 1].opaque or rest[j + 1].text not in _XARGS_FLOCK_COMMAND:
            return None
        return [rest[j + 2]] if j + 2 < len(rest) else []
    if _PYTHON_NAME.match(name):
        ipython = name.startswith("ipython")
        while k < len(rest):
            word = rest[k]
            v = word.text
            if word.opaque or v in ("-", "--") or not v.startswith("-"):
                return None
            if v.startswith("--"):
                option, eq, value = v.partition("=")
                if ipython and option == "--c":
                    string = Word.literal(value) if eq else (rest[k + 1] if k + 1 < len(rest) else None)
                    return [string] if string is not None else []
                takes = (option == "--check-hash-based-pycs" or (
                    ipython and k + 1 < len(rest) and not rest[k + 1].text.startswith("-")))
                k += 2 if takes and not eq else 1
                continue
            cluster = v[1:]
            step = 1
            for idx, c in enumerate(cluster):
                if c == "c":
                    string = _next_operand(rest, k, cluster[idx + 1:])
                    return [string] if string is not None else []
                if c == "m":
                    return None
                if c in "WX":
                    if not cluster[idx + 1:]:
                        step = 2
                    break
            k += step
        return None
    if _PERL_NAME.match(name):
        programs = []
        while k < len(rest):
            word = rest[k]
            v = word.text
            if word.opaque:
                return None
            if v == "--" or v == "-" or not v.startswith("-"):
                break
            cluster = v[1:]
            step = 1
            for idx, c in enumerate(cluster):
                if c in "eE":
                    string = _next_operand(rest, k, cluster[idx + 1:])
                    if string is None:
                        return []
                    programs.append(string)
                    step = 1 if cluster[idx + 1:] else 2
                    break
                if c in "IMmxiCdDF":
                    break  # an option whose value is the rest of the cluster
            k += step
        return programs or None
    if name in _AWK_NAMES or name in ("sed", "gsed"):
        if name in _AWK_NAMES:
            programs, files = _awk_programs(rest)[:2]
        else:
            programs, files = _sed_programs(rest)[:2]
        if programs is None or files:
            return None
        return programs
    return None


def _xargs_input_program(argv):
    """Round 26 (qanorm25 F1): whether argv runs, behind xargs and the wrappers it knows, a command whose
    program operand is missing or holds an xargs replace string, so that its program is the input xargs
    reads (printf 'rm x' | xargs -0 -I{} sh -c '{}', xargs -0 su -c, xargs -0 python3 -c, xargs -0 awk)."""
    for idx in range(1, len(argv)):
        word = argv[idx]
        if word.opaque:
            continue
        name = _basename(word.text)
        if not (name in SHELL_NAMES or name in ("su", "flock", "sed", "gsed") or name in _AWK_NAMES
                or _PYTHON_NAME.match(name) or _PERL_NAME.match(name)):
            continue
        probe = Word.literal("")
        reached = _inner_command(list(argv[:idx]) + [probe])
        if not reached or reached[0] is not probe:
            continue
        replace = None
        for x in range(idx):
            if not argv[x].opaque and _basename(argv[x].text) in _XARGS_NAMES:
                rest = argv[x + 1:]
                j = _parse_options(WRAPPERS["xargs"], rest)[0]
                replace = (replace or []) + _xargs_replace_strings(rest[:j])
        if replace is None:
            continue
        operands = _xargs_program_operands(argv[idx:])
        if operands is None:
            continue
        if not operands:
            return True
        if any(r in w.text or r in w.raw for w in operands for r in replace):
            return True
    return False


# Round 27 (qanorm26 F1, F2, F3): the whole class. xargs passes what it reads to the program it runs, as
# appended operands or in place of a replace string, and a program that can run code or commands it is
# given may run that input whatever its own operands are (sh -c '$0', python3 -c 'exec(sys.argv[1])',
# perl -e 'eval shift', awk 'BEGIN{system(ARGV[1])}', ssh host '{}', git rebase -x '{}', find . -exec sh
# -c '{}' \;, uv run sh -c {}, env, sudo, nice, timeout). Such a program behind xargs is read as running
# the input xargs reads.
_XARGS_CODE_NAMES = frozenset(("git", "jobs", "at", "batch", "source", "."))


def _xargs_code_runner(name):
    """Round 27: whether a program behind xargs can run code or commands it is given: a shell, su, an
    interpreter (python, ipython, perl, awk, sed), find or fd, ssh, eval, git, at or batch, or a wrapper
    or runner the guard knows (env, sudo, doas, nice, timeout, flock, uv, pipx, poetry and the rest)."""
    return _starts_known_argv(name) or _is_program_reader(name) or name in _XARGS_CODE_NAMES


def _xargs_arg_files(words):
    """Round 27 (qanorm26 F3): the -a FILE, -aFILE, --arg-file FILE and --arg-file=FILE values among
    xargs options words, which _parse_options has read (as words; an attached value as a literal)."""
    spec = WRAPPERS["xargs"]
    found = []
    k = 0
    while k < len(words):
        word = words[k]
        v = word.text
        if word.opaque or v == "--":
            break
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            matches = _long_matches(name, spec.long_args | spec.long_flags)
            if matches == {"--arg-file"}:
                found.append(Word(value, word.raw, word.quoted, word.opaque) if eq
                             else (words[k + 1] if k + 1 < len(words) else None))
            k += 2 if matches and matches <= spec.long_args and not eq else 1
            continue
        cluster = v[1:]
        step = 1
        for idx, c in enumerate(cluster):
            value = cluster[idx + 1:]
            if c in spec.args:
                if c == "a":
                    found.append(_next_operand(words, k, value))
                if not value:
                    step = 2
                break
            if c in spec.optargs:
                break
        k += step
    return [w for w in found if w is not None]


def _xargs_runs_code(argv, fed, written):
    """Round 27 (qanorm26 F1, F2, F3): whether argv holds an xargs whose input is fed (the command feeds
    an input anywhere, or xargs reads with -a or --arg-file in a command that writes any file, round 28)
    and that runs a program
    which can run code or commands it is given (_xargs_code_runner), whatever that program's operands
    are. The program counts when it is such a word, an expansion, or a command word it has no rule for
    with a later unquoted word that names one (it may be a wrapper it does not know); an xargs option it
    cannot read counts when any later word is such a word or an expansion. Not an xargs word that is an
    operand of a bash builtin that never runs one (echo xargs sh)."""
    head = _inner_command(argv)
    if head is None:
        head = [w for w in argv]
        while head and _is_assignment(head[0].raw):
            head = head[1:]
    if head and not head[0].opaque and _basename(head[0].text) in _INERT_BUILTINS:
        return False
    for idx, word in enumerate(argv):
        if word.opaque or _basename(word.text) not in _XARGS_NAMES:
            continue
        rest = argv[idx + 1:]
        j, ok = _parse_options(WRAPPERS["xargs"], rest)[:2]
        # round 28 (qanorm27 N1): an -a or --arg-file value counts whenever the command writes any file, as
        # the round 20 script rule does, not only when its path text matches a written path (cd /tmp, ~/,
        # cp or mv to another name)
        reads_written = bool(written) and bool(_xargs_arg_files(rest[:j] if ok else rest))
        if not (fed or reads_written):
            continue
        if not ok:
            if any(w.opaque or (not w.quoted and _xargs_code_runner(_basename(w.text))) for w in rest):
                return True
            continue
        program = rest[j:]
        if not program:
            continue  # xargs runs echo
        if program[0].opaque:
            return True
        name = _basename(program[0].text)
        if _xargs_code_runner(name):
            return True
        if not _has_rule(name) and any(not w.quoted and not w.opaque and _xargs_code_runner(_basename(w.text))
                                       for w in program[1:]):
            return True
    return False


# Round 28 (qanorm27 N2): GNU parallel, sem (parallel --semaphore), xe and rush run a command once per input
# item, as xargs does, and parallel and sem also take their items from ::: arguments and :::: files.
# Parallel, sem and rush run their command line through a shell, and parallel with no command runs each
# item as a command. Round 28 did not read their options; round 29 does (_parallel_options).
_PARALLEL_NAMES = frozenset(("parallel", "sem", "xe", "rush"))
_PARALLEL_SEPARATORS = frozenset((":::", ":::+", "::::", "::::+"))
_PARALLEL_SPLIT = re.compile(r"[\s;&|()<>`]+")
# Round 29 (qanorm28 findings 2 to 6): the guard reads their options. Option letters and long options
# that take no separate value; any other option is read as taking the next word as its value, so an
# unknown flag makes the guard read the next word as a value, not as the command word (the safe
# direction). xe: -0 -F -L -R -a -k -n -p -q -v are flags; -s SCRIPT runs SCRIPT through sh with the
# items as its arguments; -a and -A take the items from the command line (inference from xe's and GNU
# parallel's documentation, not witnessed).
# Round 42 (qanorm41 F1): round 29's short flag lists read every option they did not name as taking the
# next word, so a plain flag the lists missed (parallel -o, --tty, --silent, -x, --resume) swallowed the
# command word. Round 42 put the options of parallel, sem, xe and rush in one table, PATH_APPENDERS,
# read by _parallel_options. Each entry is recalled from that tool's documentation (no manual page was
# read in rounds 42 and 43 and none of it is witnessed): GNU parallel(1), whose sem is parallel
# --semaphore with the same options, parses with Perl's Getopt::Long (single-letter options bundled, a
# value attached or as the next word, long options also by an unambiguous prefix, options ending at the
# first word that is not one); xe(1) (getopt, short options only); rush (Go pflag: -n VALUE, -nVALUE,
# --name VALUE, --name=VALUE). For each: the letters and long options that take no value (flags,
# long_flags), that take one (args, long_args), and that take an optional one (optargs, long_optargs: read
# as taking none). Round 43 (qanorm42 N1 to N3, N6): the table no longer decides whether a git command
# behind these programs is denied (_appended_git_check reads no option table); it decides only where
# _parallel_runs_code reads the command word of the round 28 class, and an option it does not list is
# still read there as taking the next word. Round 42's placement entries, its xargs and gxargs entries
# (xargs reads WRAPPERS["xargs"]), its unsure reading and its shell-line check are gone. Round 46
# (qanorm45 F1, F2, F4): _appended_parallel_start also reads it, strictly, to find the command word that
# _appended_command_check holds to _APPENDED_PLAIN_PROGRAMS; an option it does not settle is cannot-parse.
_PARALLEL_SPEC = _Spec(
    flags="0ghkmMopqrtuvVxX", args="aCdEIjJLnNPsS", optargs="Deil",
    long_args=("--arg-file", "--arg-file-sep", "--arg-sep", "--basefile", "--bf", "--block", "--block-size",
               "--blocktimeout", "--bt", "--colsep", "--compress-program", "--decompress-program",
               "--ctagstring", "--delay", "--delimiter", "--env", "--filter", "--group-by", "--halt-on-error",
               "--halt", "--header", "--jobs", "--max-procs", "--joblog", "--limit", "--load", "--max-args",
               "--max-replace-args", "--max-chars", "--memfree", "--memsuspend", "--minversion", "--nice",
               "--profile", "--recstart", "--recend", "--results", "--res", "--retries", "--return", "--rpl",
               "--semaphorename", "--id", "--semaphoretimeout", "--st", "--seqreplace", "--slotreplace",
               "--shard", "--shell-completion", "--sql", "--sqlmaster", "--sqlandworker", "--sqlworker",
               "--ssh", "--ssh-delay", "--sshdelay", "--sshlogin", "--sshloginfile", "--slf", "--tagstring",
               "--template", "--tmpl", "--term-seq", "--timeout", "--tmpdir", "--tempdir", "--total-jobs",
               "--total", "--trc", "--transferfile", "--tf", "--trim", "--workdir", "--wd",
               "--basenamereplace", "--bnr", "--dirnamereplace", "--dnr", "--basenameextensionreplace",
               "--bner", "--extensionreplace", "--er", "--parens", "--match"),
    long_flags=("--null", "--bar", "--bibtex", "--cat", "--citation", "--cleanup", "--color", "--color-failed",
                "--cf", "--compress", "--controlmaster", "--csv", "--ctag", "--dry-run", "--dryrun", "--embed",
                "--eta", "--exit", "--fg", "--bg", "--fifo", "--files", "--files0", "--filter-hosts", "--group",
                "--hostgroups", "--hgrp", "--interactive", "--keep-order", "--no-keep-order", "--latest-line",
                "--ll", "--line-buffer", "--lb", "--link", "--xapply", "--max-line-length-allowed",
                "--no-notice", "--no-run-if-empty", "--nonall", "--onall", "--noswap", "--number-of-cpus",
                "--number-of-cores", "--number-of-threads", "--number-of-sockets", "--open-tty",
                "--output-as-files", "--outputasfiles", "--pipe", "--spreadstdin", "--pipepart",
                "--pipe-part", "--plain", "--plus", "--progress", "--quote", "--record-env", "--regexp",
                "--remove-rec-sep", "--removerecsep", "--rrs", "--resume", "--resume-failed", "--retry-failed",
                "--round-robin", "--round", "--semaphore", "--session", "--shebang", "--hashbang",
                "--shebang-wrap", "--shellquote", "--shuf", "--silent", "--skip-first-line", "--tag", "--tee",
                "--tmux", "--tmuxpane", "--transfer", "--tty", "--ungroup", "--use-cores-instead-of-threads",
                "--use-cpus-instead-of-cores", "--use-sockets-instead-of-threads", "--verbose", "--wait",
                "--will-cite", "--xargs"),
    long_optargs=("--replace", "--eof", "--max-lines", "--debug"))
PATH_APPENDERS = {
    "parallel": _PARALLEL_SPEC,
    "sem": _PARALLEL_SPEC,
    # xe [-0FLRnqv] [-p | -I replace-arg] [-N maxargs] [-j maxjobs] [-s shellscript] [-a | -A argsep]
    # [-f argfile] command...; -k and -a as round 29 read them. Round 47 (qanorm46 B1): -p is read as a
    # plain flag, so in pattern mode the first pattern is taken as the command word and the command
    # after each + is not read (see RESIDUAL)
    "xe": _Spec(flags="0FLRaknpqv", args="AfIjNs"),
    "rush": _Spec(flags="ckehV", args="vCdDIjJnortT",
                  long_args=("--assign", "--cleanup-time", "--succ-cmd-file", "--field-delimiter",
                             "--record-delimiter", "--infile", "--jobs", "--records-join-sep", "--nrecords",
                             "--out-file", "--retries", "--retry-interval", "--timeout", "--trim", "--eof",
                             "--no-kill-exes", "--no-stop-exes"),
                  long_flags=("--continue", "--dry-run", "--eta", "--keep-order", "--stop-on-error",
                              "--verbose", "--immediate-output")),
}
_PARALLEL_SEGMENT = re.compile(r"\$\(|&&|\|\||[;&|()`\n]")
_PARALLEL_REPLACE = re.compile(r"\{[^{}\s]*\}\Z|\{=.*=\}\Z")


def _unquoted_piece(text):
    """Round 29 (qanorm28 finding 4): a piece of a parallel command line with the quotes and backslashes
    removed that the shell running that line removes ("sh" and s\\h are sh)."""
    return text.replace('"', "").replace("'", "").replace("\\", "")


def _parallel_options(tool, command):
    """Round 29: read the options of a GNU parallel, sem, xe or rush command (its words before the first
    ::: or ::::); return (index of the command word or None, replacement strings from -I or --replace=,
    xe -s script words, whether xe -a or -A takes the items from the command line). Round 42 (qanorm41
    F1): through PATH_APPENDERS; an option the table does not settle is read as taking the next word as
    its value, as in round 29. Round 43 (qanorm42 N6): round 42's unsure result, which only the appended
    check read, is gone."""
    spec = PATH_APPENDERS[tool]
    replace = []
    scripts = []
    from_args = False
    k = 0
    while k < len(command):
        word = command[k]
        v = word.text
        if word.opaque:
            return k, replace, scripts, from_args
        if v == "--":
            return (k + 1 if k + 1 < len(command) else None), replace, scripts, from_args
        if not v.startswith("-") or v == "-":
            if v.isdigit():  # round 28: a number is not a command word
                k += 1
                continue
            return k, replace, scripts, from_args
        letter = None
        takes = False
        if v.startswith("--"):
            name, eq, value = v.partition("=")
            matches = _long_matches(name, spec.long_args | spec.long_flags | spec.long_optargs)
            if eq and "--replace" in matches:
                replace.append(value)
            if not matches or not (matches <= spec.long_args or matches <= spec.long_flags
                                   or matches <= spec.long_optargs):
                takes = not eq  # an option the table does not list, or a prefix of options of two kinds
            elif not eq and matches <= spec.long_args:
                takes = True
        else:
            for idx in range(1, len(v)):
                c = v[idx]
                if tool == "xe" and c in "aA":
                    from_args = True
                if c in spec.flags:
                    continue
                value = v[idx + 1:]
                if value:
                    if c == "I":
                        replace.append(value)
                    if tool == "xe" and c == "s":
                        scripts.append(Word(value, word.raw, word.quoted, word.opaque))
                elif c not in spec.optargs:
                    takes = True
                    letter = c
                break
        if takes and k + 1 < len(command):
            nxt = command[k + 1]
            if letter == "I":
                replace.append(nxt.text)
            if tool == "xe" and letter == "s":
                scripts.append(nxt)
            k += 2
            continue
        k += 1
    return None, replace, scripts, from_args


def _parallel_heads(words):
    """Round 29: the words of a command line that the shell running it reads as command words: the first
    word of the line and of each part after a shell operator or $( or a backquote, unquoted."""
    heads = []
    for part in _PARALLEL_SEGMENT.split(" ".join(w.text for w in words)):
        pieces = part.split()
        if pieces:
            heads.append(_unquoted_piece(pieces[0]))
    return heads


def _parallel_runs_code(argv, fed, written):
    """Round 28 (qanorm27 N2): whether argv holds a GNU parallel, sem, xe or rush whose input is fed (the
    command feeds an input anywhere, writes any file, which an arg-file option or :::: may read, or, for
    parallel and sem, has a ::: or :::: argument source) and whose command may run code or commands it is
    given: a word before the first ::: or :::: is an expansion, or holds, split at blanks and shell
    operators, a word that names a program that can run code (_xargs_code_runner), quoted or not, since
    the command line is run through a shell; or, for parallel and sem, no word there is a command word
    (each starts with - or is a number), since parallel then runs each input item as a command; or the
    program is rush, which runs its command line (by default echo {}) through a shell with each item put
    in place of its replacement strings (inference from rush's documentation, not witnessed). Round 29
    (qanorm28): a piece counts with its quotes and backslashes removed ("sh", s\\h), and so does a
    command substitution in a word; an option value given as a separate word is not a command word
    (parallel -a c.txt has none); xe -s runs its script through sh; a replacement string, the -I or
    --replace= value, or an expansion as a command word of the line runs each item as a command
    (parallel {}, parallel -I@ @); and, whatever the input, a removal command name as a command word of
    the line or of an xe -s script, quoted or not, or a round 15 removal form in it (parallel 'rm {}',
    xe 'rm'). Not such a word that is an operand of a bash builtin that never runs one (echo parallel
    sh)."""
    head = _inner_command(argv)
    if head is None:
        head = [w for w in argv]
        while head and _is_assignment(head[0].raw):
            head = head[1:]
    if head and not head[0].opaque and _basename(head[0].text) in _INERT_BUILTINS:
        return False
    for idx, word in enumerate(argv):
        if word.opaque:
            continue
        tool = _basename(word.text)
        if tool not in _PARALLEL_NAMES:
            continue
        rest = argv[idx + 1:]
        cut = next((k for k, w in enumerate(rest) if not w.opaque and w.text in _PARALLEL_SEPARATORS),
                   len(rest))
        command = rest[:cut]
        start, replace, scripts, from_args = _parallel_options(tool, command)
        line = command[start:] if start is not None else []
        heads = _parallel_heads(line) + [h for s in scripts for h in _parallel_heads([s])]
        # round 29 (qanorm28 finding 5): a removal command name that the command line runs, quoted or not,
        # or a round 15 removal form in it, whatever the input (parallel 'rm {}', xe 'rm', as xargs 'rm')
        forms = [" ".join(w.text for w in line)] + [s.text for s in scripts]
        if any(_basename(h) in REMOVERS for h in heads) or any(_has_removal_form_text(f) for f in forms):
            return True
        has_source = (tool in ("parallel", "sem") and cut < len(rest)) or (tool == "xe" and from_args)
        if not (fed or written or has_source):
            continue
        if tool == "rush":
            return True
        # round 29 (qanorm28 finding 2): xe -s runs its script through sh with the items as arguments
        if scripts:
            return True
        if any(w.opaque for w in command):
            return True
        # round 29 (qanorm28 finding 4): quotes and backslashes in a piece, and a command substitution
        if any(_xargs_code_runner(_basename(_unquoted_piece(piece)))
               for w in command for piece in _PARALLEL_SPLIT.split(w.text) if piece):
            return True
        if any("$(" in w.text or "`" in w.text for w in command):
            return True
        # round 28, and round 29 (qanorm28 finding 5): parallel or sem with no command word, also when
        # an option value is a separate word (parallel -a c.txt, parallel --joblog log)
        if tool in ("parallel", "sem") and start is None:
            return True
        # round 29 (line-178 MINOR of qanorm28): a replacement string (or an expansion) as a command word
        # runs each item as a command (parallel {}, parallel -I@ @, sem {})
        if any(h.startswith("$") or _PARALLEL_REPLACE.match(h) or h in replace for h in heads):
            return True
    return False


def _program_input_scan(token_lists, argvs, command, depth):
    """Deny (cannot parse) when the command text holds a removal word or a round 15 removal form anywhere,
    and a shell, at, batch, python, perl, source or . in it runs a program read from its standard input
    or from a process-substitution or standard-input path, and the command feeds an input; (round 27)
    or when an xargs in it whose input is fed runs a program that can run code or commands it is given."""
    if not (_has_removal_text(command) or _has_removal_form_text(command)):
        return None
    fed = _feeds_input(token_lists)
    written = None
    for argv in argvs:
        # round 26 (qanorm25 F1): or a program operand that xargs fills from its input
        if fed and (_reads_program_input(argv, depth) or _xargs_input_program(argv)):
            return CANNOT_PARSE
        # round 27 (qanorm26 F1, F2, F3): or any program behind a fed xargs that can run code
        if any(not w.opaque and _basename(w.text) in _XARGS_NAMES for w in argv):
            if written is None:
                written = _written_files(token_lists, argvs)
            if _xargs_runs_code(argv, fed, written):
                return CANNOT_PARSE
        # round 28 (qanorm27 N2): or the same class behind GNU parallel, sem, xe or rush
        if any(not w.opaque and _basename(w.text) in _PARALLEL_NAMES for w in argv):
            if written is None:
                written = _written_files(token_lists, argvs)
            if _parallel_runs_code(argv, fed, written):
                return CANNOT_PARSE
    return None


# Round 20 (qanorm19 MEDIUM-2): a script written and run in the same command (echo 'rm -rf x' > c.sh &&
# bash c.sh) has its contents in the command text. A reader given a script operand (a shell, python,
# perl, awk -f, sed -f, source or . with a file), or a command word that is a path the command writes,
# in a command that writes a file (an output redirection to a file other than /dev/null, /dev/zero,
# /dev/tty, /dev/stdout or /dev/stderr, tee, or round 29 cp, mv, install, ln or dd of=) and holds a
# removal word or a round 15 removal form anywhere, denies as cannot-parse.
_WRITE_OPS = frozenset((">", ">>", ">|", "&>", "&>>", ">&"))
# Round 29 (qanorm28 finding 1): a /dev/ path is a written file (/dev/shm and /dev/mqueue hold files that
# persist, and /dev/fd/N may name one), except these character devices, which cannot hold a script
_UNWRITTEN_DEVICES = frozenset(("/dev/null", "/dev/zero", "/dev/tty", "/dev/stdout", "/dev/stderr"))
# Round 29 (qanorm28 findings 2 and 6): programs that write a file named among their operands, and the
# words of a python or perl program that may write a file
_COPY_PROGRAMS = frozenset(("cp", "mv", "install", "ln"))
_INTERPRETER_WRITE = re.compile(r"\bopen\b|write|\bcopy|\bmove|\brename|\bsymlink|\blink\b|\bsystem\b")


def _written_files(token_lists, argvs):
    """The words the command writes as files: the target of >, >>, >|, &>, &>> or >& WORD (not a file
    descriptor number or -), every operand of tee, (round 29) every operand of cp, mv, install or ln that
    is not an option and the of= value of dd; /dev/null, /dev/zero, /dev/tty, /dev/stdout and
    /dev/stderr are not files it writes (round 29: any other /dev/ path is)."""
    targets = []
    for tokens in token_lists:
        for idx, (kind, val) in enumerate(tokens):
            if kind != "op" or val not in _WRITE_OPS or idx + 1 >= len(tokens) or tokens[idx + 1][0] != "w":
                continue
            target = tokens[idx + 1][1]
            if val == ">&" and not target.opaque and (target.text.isdigit() or target.text == "-"):
                continue
            targets.append(target)
    for argv in argvs:
        words = _inner_command(argv)
        if words is None:
            words = argv
        if not words or words[0].opaque:
            continue
        name = _basename(words[0].text)
        if name == "tee" or name in _COPY_PROGRAMS:
            targets.extend(w for w in words[1:] if w.opaque or not w.text.startswith("-"))
        elif name == "dd":
            targets.extend(w if w.opaque else Word(w.text[3:], w.raw, w.quoted, w.opaque)
                           for w in words[1:] if w.text.startswith("of="))
        elif _PYTHON_NAME.match(name) or _PERL_NAME.match(name):
            # round 29 (qanorm28 finding 6): a python -c or perl -e program that may write a file writes
            # one whose path the guard does not read
            programs = _xargs_program_operands(words) or []
            if any(op.opaque or _INTERPRETER_WRITE.search(op.text) for op in programs):
                targets.append(Word("", "", False, True))
    return [t for t in targets if t.opaque or os.path.normpath(t.text) not in _UNWRITTEN_DEVICES]


def _written_script_scan(token_lists, argvs, command, depth):
    if not (_has_removal_text(command) or _has_removal_form_text(command)):
        return None
    written = _written_files(token_lists, argvs)
    if not written:
        return None
    paths = set(os.path.normpath(t.text) for t in written if not t.opaque)
    for argv in argvs:
        if _program_source(argv, depth)[1] is not None:
            return CANNOT_PARSE
        words = _inner_command(argv)
        if words and not words[0].opaque and "/" in words[0].text and (
                os.path.normpath(words[0].text) in paths or any(t.opaque for t in written)):
            return CANNOT_PARSE
        # round 29 (qanorm28 finding 6): a shell or su -c string that runs a reader, xargs, source or .,
        # or a path the command writes (echo 'rm x' > c.sh; sh -c 'sh c.sh')
        if words and not words[0].opaque and (_basename(words[0].text) in SHELL_NAMES
                                              or _basename(words[0].text) == "su"):
            for op in _xargs_program_operands(words) or []:
                pieces = [p for p in _READER_SPLIT.split(op.text) if p]
                if op.opaque or _names_reader(op.text) or any(
                        _basename(p) in ("xargs", "gxargs", ".") or os.path.normpath(p) in paths
                        for p in pieces):
                    return CANNOT_PARSE
    return None


def _check_command_text(command, depth, forms=False):
    """Check a whole command string; return DENY, CANNOT_PARSE or None. With forms (a shell -c string), a
    round 15 removal form in the text counts as a removal word for the cannot-parse tests."""
    def holds(text):
        return _has_removal_text(text) or (forms and _has_removal_form_text(text))

    if depth == 0:
        _command_text[0] = command  # round 46: the text _appended_command_check scans for settings
    ctx = _Ctx()
    try:
        tokens, _end = _lex(ctx, command, 0, False)
        argvs = []
        for token_list in [tokens] + ctx.subs:
            argvs.extend(_command_argvs(token_list))
    except ParseError:
        if holds(command):
            return CANNOT_PARSE
        # Round 22 (qanorm21 N1): a top-level command it cannot parse (a named coproc, case inside $( ),
        # an extglob pattern) with a round 15 removal form in the text, as for a shell -c string
        if depth == 0 and _has_removal_form_text(command):
            return CANNOT_PARSE
        # Round 19: a reader named in a command it cannot parse, with a round 15 removal form in the text
        return CANNOT_PARSE if _has_removal_form_text(command) and _names_reader(command) else None
    uncertain = False
    for argv in argvs:
        result = _check_argv(argv, depth, getattr(argv, "assigns", ()))
        if result == DENY:
            return DENY
        if result == CANNOT_PARSE:
            uncertain = True
    # Round 18 (qanorm17 M2), round 19 (qanorm18 MAJOR-1, MAJOR-2, MEDIUM-2): a program read from stdin or
    # a process-substitution or standard-input path; its removal word or round 15 removal form counts
    # wherever it is in the command text
    if not uncertain and _program_input_scan([tokens] + ctx.subs, argvs, command, depth):
        uncertain = True
    # Round 20 (qanorm19 MEDIUM-2): a script written to a file and run in the same command
    if not uncertain and _written_script_scan([tokens] + ctx.subs, argvs, command, depth):
        uncertain = True
    if not uncertain and holds(command) and _unreadable_constructs(ctx, command, argvs):
        uncertain = True
    # Round 32 (D-2384): a here-document body with a removal command in command position
    if not uncertain and _HEREDOC_REMOVAL in ctx.unreadable:
        uncertain = True
    # Round 34 (qanorm33 N3): an interpreter program that an expansion supplies
    if (not uncertain and _RULES["interpreter program expansion"] and holds(command)
            and _expanded_program(argvs)):
        uncertain = True
    return CANNOT_PARSE if uncertain else None


def _expanded_program(argvs):
    """Round 34 (qanorm33 N3): whether a shell, su, python or perl argv (behind the wrappers it knows) takes
    its -c or -e program from a word that holds an expansion (python3 -c "$(cat <<'PY' ... PY\\n)",
    x=$(cat <<'PY' ... ); python3 -c "$x"): round 32 reads a here-document body as data, so such a program
    is text the inner layer does not read; with a removal word anywhere in the command it denies as
    cannot-parse."""
    for argv in argvs:
        words = _inner_command(argv)
        if not words or words[0].opaque:
            continue
        name = _basename(words[0].text)
        if not (name in SHELL_NAMES or name == "su" or _PYTHON_NAME.match(name) or _PERL_NAME.match(name)):
            continue
        if any(op is not None and op.opaque for op in _xargs_program_operands(words) or []):
            return True
    return False


# --- round 32: the here-document body test and the broad outer layer (D-2385, D-2384) ----------------

# A here-document body line is split into segments at these shell operators; the first word of each
# segment (after NAME=VALUE words and the reserved words in _BODY_SKIP) is in command position.
_BODY_SEGMENT = re.compile(r"&&|\|\||\$\(|[;&|(){}`]")
_BODY_SKIP = frozenset(("!", "if", "then", "elif", "else", "do", "while", "until", "time"))
_BODY_RUNNERS = frozenset(("git", "cargo", "rsync", "gio", "xargs", "gxargs", "parallel", "sem", "xe", "rush",
                           "jobs", "source", "."))


def _body_runs_removal(body):
    """Whether a here-document body holds a removal command in command position: a segment whose command
    word is a removal command name (rm, rmdir, unlink, shred, srm, wipe, also as a path), or is a shell,
    su, interpreter, find, fd, ssh, eval, wrapper or runner the guard knows, or git, cargo, rsync, gio,
    xargs, parallel, sem, xe, rush, jobs, source or ., when the line from that segment on holds a
    removal word or a round 15 removal form (the split does not read quotes, so a quoted ; or ( may
    end a segment early)."""
    for line in body.split("\n"):
        starts = [0] + [m.end() for m in _BODY_SEGMENT.finditer(line)]
        for k, start in enumerate(starts):
            end = (_BODY_SEGMENT.search(line, start).start() if k + 1 < len(starts) else len(line))
            words = [_STRIP_QUOTING.sub("", w) for w in line[start:end].split()]
            j = 0
            while j < len(words) and (words[j] in _BODY_SKIP or _ASSIGN_RE.match(words[j])):
                j += 1
            if j >= len(words):
                continue
            name = _basename(words[j])
            if name in REMOVERS:
                return True
            rest = line[start:]
            if (_starts_known_argv(name) or name in _BODY_RUNNERS) and (
                    _has_removal_text(rest) or _has_removal_form_text(rest)):
                return True
    return False


# Round 33 (qanorm32 F2): a redirection word (with its fd number) that may come before a command word,
# and a segment split that keeps &, | and >& inside such a word (2>&1, &>f, >|f)
_BODY_REDIRECT = re.compile(r"(?:[0-9]+|\{[A-Za-z_][A-Za-z0-9_]*\})?(?:&>>?|>>?\|?|<<?-?|<>|[<>]&)")
_BODY_SEGMENT_KEEP_REDIRECT = re.compile(r"&&|\|\||\$\(|[;(){}`]|(?<![<>])&(?!>)|(?<!>)\|")


def _body_command_word_runs(name, rest):
    """The command-position name test of _body_runs_removal for one command word."""
    return name in REMOVERS or ((_starts_known_argv(name) or name in _BODY_RUNNERS) and (
        _has_removal_text(rest) or _has_removal_form_text(rest)))


def _body_command_words_run_removal(body):
    """Round 33 (qanorm32 F2): the command-position test on every command word the inner layer finds.
    The whole body and each body line that the lexer reads are split into simple commands by
    _command_argvs itself, which skips redirections, NAME=VALUE words and the reserved words it knows
    (!, coproc, time and time -p, if, then, elif, else, do, while, until, {, a case pattern), and a
    here-document nested in the body counts as it does at the top. A line the lexer cannot read is split
    as text, as in _body_runs_removal, but without splitting a redirection (2>&1, &>f) and skipping
    redirection words with their targets, coproc and time options before the command word. A command
    word built at run time and one the guard does not name are not read (see RESIDUAL)."""
    for text in [body] + body.split("\n"):
        ctx = _Ctx()
        try:
            tokens, _end = _lex(ctx, text, 0, False)
            argvs = []
            for token_list in [tokens] + ctx.subs:
                argvs.extend(_command_argvs(token_list))
        except ParseError:
            continue
        if _HEREDOC_REMOVAL in ctx.unreadable:
            return True
        for argv in argvs:
            if not argv or argv[0].opaque:
                continue
            span = argv[0].span
            known = span is not None and text[span[0]:span[1]] == argv[0].raw
            if _body_command_word_runs(_basename(argv[0].text), text[span[0]:] if known else text):
                return True
    for line in body.split("\n"):
        starts = [0] + [m.end() for m in _BODY_SEGMENT_KEEP_REDIRECT.finditer(line)]
        for k, start in enumerate(starts):
            end = (_BODY_SEGMENT_KEEP_REDIRECT.search(line, start).start() if k + 1 < len(starts)
                   else len(line))
            words = [_STRIP_QUOTING.sub("", w) for w in line[start:end].split()]
            j = 0
            timed = False
            while j < len(words):
                word = words[j]
                redirect = _BODY_REDIRECT.match(word)
                if redirect:
                    j += 2 if redirect.end() == len(word) else 1
                    continue
                if word in _BODY_SKIP or word == "coproc" or _ASSIGN_RE.match(word) or (
                        timed and word.startswith("-")):
                    timed = timed or word == "time"
                    j += 1
                    continue
                break
            if j < len(words) and _body_command_word_runs(_basename(words[j]), line[start:]):
                return True
    return False


_GIT_COMMIT_VALUE_OPTIONS = frozenset(("-c", "-C", "-t", "--template", "--author", "--date", "--fixup",
                                       "--squash", "--trailer", "--cleanup", "--reuse-message",
                                       "--reedit-message", "--pathspec-from-file"))
_GREP_SPEC = ("ABCDdefm", "abcEFGHhIiLlnoPqRrsTUuVvwxyZz",
              frozenset(("--after-context", "--before-context", "--context", "--devices", "--directories",
                         "--regexp", "--file", "--max-count", "--label", "--include", "--exclude",
                         "--exclude-dir", "--exclude-from", "--binary-files", "--group-separator")),
              frozenset(("--recursive", "--dereference-recursive", "--ignore-case", "--no-ignore-case",
                         "--line-number", "--files-with-matches", "--files-without-match", "--count",
                         "--invert-match", "--word-regexp", "--line-regexp", "--only-matching", "--quiet",
                         "--silent", "--no-messages", "--with-filename", "--no-filename", "--extended-regexp",
                         "--fixed-strings", "--perl-regexp", "--basic-regexp", "--null-data", "--null",
                         "--text", "--byte-offset", "--initial-tab", "--line-buffered",
                         "--no-group-separator", "--color", "--colour")))
_RG_SPEC = ("ABCdEefgjMmrtT", "0.abcFHhIiLlNnopPqSsUuVvwxz",
            frozenset(("--after-context", "--before-context", "--context", "--regexp", "--file", "--glob",
                       "--iglob", "--type", "--type-not", "--type-add", "--type-clear", "--max-count",
                       "--max-depth", "--maxdepth", "--threads", "--encoding", "--max-columns", "--replace",
                       "--colors", "--color", "--sort", "--sortr", "--pre", "--pre-glob", "--ignore-file",
                       "--max-filesize", "--path-separator", "--engine", "--context-separator",
                       "--field-match-separator", "--field-context-separator", "--dfa-size-limit",
                       "--regex-size-limit", "--generate", "--hostname-bin", "--hyperlink-format")),
            frozenset(("--hidden", "--no-ignore", "--ignore-case", "--smart-case", "--case-sensitive",
                       "--fixed-strings", "--word-regexp", "--line-regexp", "--line-number",
                       "--no-line-number", "--files-with-matches", "--files-without-match", "--count",
                       "--count-matches", "--invert-match", "--only-matching", "--quiet", "--follow",
                       "--multiline", "--multiline-dotall", "--pcre2", "--no-heading", "--heading",
                       "--with-filename", "--no-filename", "--json", "--vimgrep", "--unrestricted", "--text",
                       "--null", "--null-data", "--trim", "--stats", "--passthru", "--column", "--no-messages",
                       "--byte-offset", "--search-zip", "--crlf", "--no-config", "--no-ignore-vcs",
                       "--no-ignore-parent", "--no-ignore-dot", "--no-ignore-global", "--glob-case-insensitive",
                       "--one-file-system", "--binary", "--line-buffered", "--block-buffered", "--pretty",
                       "--help", "--version")))
# A message or body word that holds an expansion is exempt only in the git commit here-document shape:
# "$(cat <<'EOF' (or <<EOF, <<-) then the body lines, the delimiter line and )" with nothing else.
_SUBSTITUTION_MARK = re.compile(r"\$[(\[{'\"]|`|[<>]\(")
_HEREDOC_MESSAGE = re.compile(
    r"(?:-[A-Za-z]|--[A-Za-z-]+=)?\"\$\(cat[ \t]+<<(-?)[ \t]*(?:'([A-Za-z_][A-Za-z0-9_]*)'|"
    r"([A-Za-z_][A-Za-z0-9_]*))[ \t]*\n(.*?)\n(\t*)(?:\2|\3)\n[ \t]*\)\"", re.S)
_SEGMENT_BREAKS = _SEPARATOR_OPS | _CASE_END_OPS | frozenset(("(", ")"))


def _next_value(words, k, exempt):
    """Add words[k + 1] to exempt when it exists; return it (or None)."""
    if k + 1 < len(words):
        exempt.append(words[k + 1])
        return words[k + 1]
    return None


def _git_commit_message_words(words):
    """The words of a git commit argv that are message text (the values of -m, --message, -F and --file),
    and whether -F or --file reads the message from standard input (-)."""
    if not words or words[0].opaque or _basename(words[0].text) != "git":
        return [], False
    j = 1
    while j < len(words):
        t = words[j].text
        if words[j].opaque:
            return [], False
        if t in GIT_VALUE_OPTIONS:
            j += 2
        elif t.startswith("--") and t.split("=", 1)[0] in GIT_VALUE_OPTIONS and "=" in t:
            j += 1
        elif t in GIT_PLAIN_OPTIONS:
            j += 1
        else:
            break
    if j >= len(words) or words[j].opaque or words[j].text != "commit":
        return [], False
    exempt = []
    stdin = False
    k = j + 1
    while k < len(words):
        w = words[k]
        t = w.text
        if w.opaque:
            k += 1
            continue
        if t == "--":
            break
        if t in ("-m", "-F", "--message", "--file"):
            value = _next_value(words, k, exempt)
            if t in ("-F", "--file") and value is not None and not value.opaque and value.text == "-":
                stdin = True
            k += 2
            continue
        if t.startswith("--message=") or t.startswith("--file="):
            exempt.append(w)
            stdin = stdin or t == "--file=-"
            k += 1
            continue
        if t in _GIT_COMMIT_VALUE_OPTIONS:
            k += 2
            continue
        if t.startswith("-") and not t.startswith("--") and len(t) > 1:
            step = 1
            for idx, ch in enumerate(t[1:], 1):
                rest = t[idx + 1:]
                if ch in "mF":
                    if rest:
                        exempt.append(w)
                        stdin = stdin or (ch == "F" and rest == "-")
                    else:
                        value = _next_value(words, k, exempt)
                        stdin = stdin or (ch == "F" and value is not None and not value.opaque
                                          and value.text == "-")
                        step = 2
                    break
                if ch in "cCt":
                    step = 1 if rest else 2
                    break
                if ch in "Su":
                    break
            k += step
            continue
        k += 1
    return exempt, stdin


def _gh_body_words(words):
    """The words of a gh pr or gh issue argv that are body text (the values of -b, --body, -F and
    --body-file), and whether -F or --body-file reads the body from standard input (-)."""
    if (len(words) < 3 or words[0].opaque or words[1].opaque or _basename(words[0].text) != "gh"
            or words[1].text not in ("pr", "issue")):
        return [], False
    exempt = []
    stdin = False
    k = 2
    while k < len(words):
        w = words[k]
        t = w.text
        if w.opaque:
            k += 1
            continue
        if t == "--":
            break
        if t in ("-b", "--body", "-F", "--body-file"):
            value = _next_value(words, k, exempt)
            if t in ("-F", "--body-file") and value is not None and not value.opaque and value.text == "-":
                stdin = True
            k += 2
            continue
        if t.startswith("--body=") or t.startswith("--body-file=") or (len(t) > 2 and t[:2] in ("-b", "-F")):
            exempt.append(w)
            stdin = stdin or t in ("--body-file=-", "-F-")
        k += 1
    return exempt, stdin


def _pattern_words(words):
    """The words of a grep or rg argv that are patterns: the values of -e and --regexp, or, with neither
    and no -f or --file, the first operand. An expansion, or an option it does not know (which may take
    the next word as its value), ends the reading; no operand is then a pattern. The value of a value
    option it knows (rg --pre COMMAND among them) is skipped and is not a pattern."""
    if not words or words[0].opaque:
        return []
    name = _basename(words[0].text)
    if name == "grep":
        value_short, plain_short, value_long, plain_long = _GREP_SPEC
    elif name == "rg":
        value_short, plain_short, value_long, plain_long = _RG_SPEC
    else:
        return []
    exempt = []
    explicit = False
    known = True
    positional = None
    k = 1
    while k < len(words):
        w = words[k]
        t = w.text
        if w.opaque:
            known = False
            break
        if t == "--":
            if positional is None and k + 1 < len(words):
                positional = k + 1
            break
        if t.startswith("--"):
            option, eq, _value = t.partition("=")
            if option in ("--regexp", "--file"):
                explicit = True
            if eq:
                if option == "--regexp":
                    exempt.append(w)
                k += 1
            elif option == "--regexp":
                _next_value(words, k, exempt)
                k += 2
            elif option in value_long:
                k += 2
            elif option in plain_long:
                k += 1
            else:
                known = False
                break
            continue
        if t.startswith("-") and len(t) > 1:
            step = 1
            for idx, ch in enumerate(t[1:], 1):
                rest = t[idx + 1:]
                if ch in value_short:
                    if ch in "ef":
                        explicit = True
                    if ch == "e":
                        if rest:
                            exempt.append(w)
                        else:
                            _next_value(words, k, exempt)
                    step = 1 if rest else 2
                    break
                if ch in plain_short or ch.isdigit():
                    continue
                known = False
                break
            if not known:
                break
            k += step
            continue
        if positional is None:
            positional = k
        k += 1
    if known and not explicit and positional is not None:
        exempt.append(words[positional])
    return exempt


def _exempt_ok(word, command):
    """A message, body or pattern word is exempt when its source in the command is known and it holds no
    expansion, or it is exactly the git commit here-document shape (see _HEREDOC_MESSAGE)."""
    if word.span is None or command[word.span[0]:word.span[1]] != word.raw:
        return False
    if not _SUBSTITUTION_MARK.search(word.raw):
        return True
    match = _HEREDOC_MESSAGE.fullmatch(word.raw)
    if not match:
        return False
    dash, quoted_delim, bare_delim, body, tabs = match.groups()
    delim = quoted_delim or bare_delim
    if tabs and not dash:
        return False
    # Round 33 (qanorm32 F1): bash 5.3.9 ends a here-document inside $( ) at a line that starts with the
    # delimiter followed by ) (EOF)"), which this lexer reads as body, and then runs the next line; a body
    # line that starts with the delimiter after leading spaces or tabs is refused in the safe direction
    if _RULES["here-document delimiter prefix"] and any(
            line.lstrip(" \t").startswith(delim) for line in body.split("\n")):
        return False
    if any((line.lstrip("\t") if dash else line) == delim for line in body.split("\n")):
        return False  # bash ends the here-document at that earlier line
    if bare_delim and any(c in body for c in "$`\\"):
        return False
    return True


def _segment_words(tokens, k):
    """The words of the simple command around tokens[k] (up to a separator, a newline or a parenthesis)."""
    def breaks(token):
        return token[0] == "nl" or (token[0] == "op" and token[1] in _SEGMENT_BREAKS)
    lo = k
    while lo > 0 and not breaks(tokens[lo - 1]):
        lo -= 1
    hi = k
    while hi + 1 < len(tokens) and not breaks(tokens[hi + 1]):
        hi += 1
    return [value for kind, value in tokens[lo:hi + 1] if kind == "w"]


def _without_assignments(words):
    j = 0
    while j < len(words) and _is_assignment(words[j].raw):
        j += 1
    return list(words[j:])


def _exempt_command_words(words, assigns):
    """Round 33 (qanorm32 F3): the words of a command an exception may read: with the exact command word
    rule, only a command whose first word is exactly git, gh, grep or rg, unquoted and with no NAME=VALUE
    word before it (a path such as ./git or a PATH= word may run another program)."""
    if not _RULES["exact command word"]:
        return _without_assignments(words)
    if assigns or not words or words[0].raw not in _EXEMPT_COMMAND_NAMES:
        return []
    return list(words)


_EXEMPT_COMMAND_NAMES = frozenset(("git", "gh", "grep", "rg"))
# Round 33 (qanorm32 F3, F4): outside the exempt text, the word PATH as written (a command that sets it
# may run another program for git, gh, grep or rg) and, after quote and backslash removal, a function
# definition named git, gh, grep or rg; round 34 (qanorm33 N1) also reads PATH after quote and backslash
# removal (see _path_bound)
_PATH_WORD = re.compile(r"(?<![A-Za-z0-9_])PATH(?![A-Za-z0-9_])")
_SHADOW_DEFINITION = re.compile(r"(?<![A-Za-z0-9_.-])function\s+(?:git|gh|grep|rg)(?![A-Za-z0-9_.-])"
                                r"|(?<![A-Za-z0-9_./-])(?:git|gh|grep|rg)\s*\(\s*\)")


# Round 34 (qanorm33 N1): bash builtins that bind a variable named by an operand (export PA"TH"=.,
# declare -n p=PATH, printf -v PATH, read PATH); an operand built at run time may name PATH
_NAME_BINDERS = frozenset(("export", "declare", "typeset", "local", "readonly", "read", "getopts", "mapfile",
                           "readarray", "unset"))
# Round 34 (qanorm33 N2): command words that may run exempt text that the same command stored (sh
# .git/COMMIT_EDITMSG, sh -c "$(git log -1 --format=%B)", awk '{system($0)}' f, find -exec sh {} ;)
_TEXT_RUNNERS = frozenset(("source", ".", "eval", "xargs", "gxargs", "find", "gfind", "bfs", "fd", "fdfind",
                           "sed", "gsed", "env"))
# Round 34 (qanorm33 N2): outside the exempt text, after quote and backslash removal, a git setting that
# runs a program on the message or a path to the message file git writes
_GIT_RUN_SETTING = re.compile(r"hookspath|commit_editmsg|git_config|git_exec_path|\.git/hooks|\.git/config",
                              re.I)


def _path_bound(outside, all_argvs):
    """Round 34 (qanorm33 N1): the word PATH outside the exempt text after line-continuation, quote and
    backslash removal (export PA"TH"=., declare -x PA''TH=., read -r PA\\TH), or a builtin that binds a
    variable whose name an expansion supplies (n=PA; export "${n}TH"=., printf -v "$v", declare -n p=$v)."""
    if _PATH_WORD.search(_STRIP_QUOTING.sub("", outside.replace("\\\n", ""))):
        return True
    for argv in all_argvs:
        words = _without_assignments(argv)
        if not words or words[0].opaque:
            continue
        name = words[0].text
        if name == "printf" and not any(not w.opaque and w.text.startswith("-v") for w in words[1:]):
            continue
        if (name in _NAME_BINDERS or name == "printf") and any(w.opaque for w in words[1:]):
            return True
    return False


def _git_runs_setting(words):
    """Round 34 (qanorm33 N2): whether a git argv sets configuration that may run a program (-c,
    --config-env or --exec-path before the subcommand, or git config), or is a git commit that starts the
    editor on its message (-e, --edit, -c, --reedit-message, --fixup=amend: or reword:)."""
    j = 1
    while j < len(words):
        t = words[j].text
        if words[j].opaque:
            return True
        option = t.split("=", 1)[0]
        if option in ("-c", "--config-env", "--exec-path") or t.startswith("-c"):
            return True
        if t in GIT_VALUE_OPTIONS:
            j += 2
        elif t.startswith("--") and option in GIT_VALUE_OPTIONS and "=" in t:
            j += 1
        elif t in GIT_PLAIN_OPTIONS:
            j += 1
        else:
            break
    if j >= len(words):
        return False
    sub = words[j].text
    if sub == "config":
        return True
    if sub != "commit":
        return False
    k = j + 1
    while k < len(words):
        w = words[k]
        t = w.text
        k += 1
        if w.opaque:
            continue
        if t == "--":
            break
        if t in ("-m", "-F", "--message", "--file", "-C", "-t", "--template", "--author", "--date",
                 "--squash", "--trailer", "--cleanup", "--reuse-message", "--pathspec-from-file"):
            k += 1
            continue
        if t.startswith("--"):
            option, eq, value = t.partition("=")
            if len(option) > 2 and ("--edit".startswith(option) or (
                    len(option) > 4 and "--reedit-message".startswith(option))):
                return True
            if option == "--fixup" or (len(option) > 3 and "--fixup".startswith(option)):
                if not eq:
                    value = words[k].text if k < len(words) else ""
                    k += 1
                if value.startswith("amend:") or value.startswith("reword:"):
                    return True
            continue
        if t.startswith("-") and len(t) > 1:
            for ch in t[1:]:
                if ch in "ec":
                    return True
                if ch in "mFCt":
                    if t.endswith(ch):
                        k += 1
                    break
                if ch in "Su":
                    break
    return False


def _gh_runs_editor(words):
    """Round 34 (qanorm33 N2): whether a gh argv starts the editor on its body (-e, --editor) or sets gh
    configuration (gh config, gh alias)."""
    if len(words) > 1 and not words[1].opaque and words[1].text in ("config", "alias"):
        return True
    return any(not w.opaque and (w.text in ("-e", "--editor") or w.text.startswith("--editor=")
                                 or re.fullmatch(r"-[dfw]*e[dfw]*", w.text)) for w in words[1:])


def _text_runner(argv, exempt_spans):
    """Round 34 (qanorm33 N2): whether an argv may run text the same command stored: behind the wrappers it
    knows, a shell, su, interpreter, ssh, at, source, ., eval, xargs, find, fd, sed or awk command word, or
    such a word later in the argv of git or of a command word it does not know (git bisect run sh f,
    chroot /srv sh f)."""
    def runs(name):
        return _is_program_reader(name) or name in _TEXT_RUNNERS or name in _AWK_NAMES or name in _PARALLEL_NAMES

    words = _inner_command(argv)
    if words is None:
        words = _without_assignments(argv)
    if not words:
        return False
    if words[0].opaque:
        return True
    name = _basename(words[0].text)
    if runs(name):
        return True
    if name in ("gh", "grep", "rg") or (_has_rule(name) and name != "git"):
        return False
    for w in words[1:]:
        if w.opaque or w.span in exempt_spans or w.text == ".":
            continue
        if runs(_basename(w.text)):
            return True
    return False


# Round 35 (qanorm34 N2): the broad layer's exceptions apply only to a command that is one simple command
# of these forms, each an allowlist (an option it does not name refuses the exception; a long option
# matches only as written, never as an abbreviation): (value short letters, plain short letters, value
# long options, plain long options, long options that take a value only after =)
_ALLOWLIST_EXPANSION = re.compile(r"[$`]|[<>]\(")
_GIT_COMMIT_ALLOW = ("mF", "aqsn", frozenset(("--message", "--file", "--author", "--date")),
                     frozenset(("--all", "--quiet", "--signoff", "--allow-empty", "--allow-empty-message",
                                "--amend", "--no-edit", "--no-verify")), frozenset())
_GH_ALLOW_SUBCOMMANDS = frozenset(("create", "edit", "comment"))
_GH_ALLOW = ("tbFBHlamRpT", "d",
             frozenset(("--title", "--body", "--body-file", "--base", "--head", "--label", "--assignee",
                        "--reviewer", "--milestone", "--repo", "--project", "--template", "--add-label",
                        "--remove-label", "--add-assignee", "--remove-assignee", "--add-reviewer",
                        "--remove-reviewer", "--add-project", "--remove-project")),
             frozenset(("--draft",)), frozenset())
# grep runs no program for any option it knows (_GREP_SPEC); --color and --colour take a value only after =
_GREP_ALLOW = _GREP_SPEC + (frozenset(("--color", "--colour")),)
# rg: no --pre, --pre-glob, --hostname-bin or -z/--search-zip, each of which runs a program. Round 36
# (qanorm35 R2): every short option here has its long spelling here, and the reverse, so the two spellings
# get the same verdict (_RG_SPELLING_PAIRS)
_RG_ALLOW = ("ABCdEefgjMmrtT", "0.abcFHhIiLlNnopPqSsUuVvwx",
             frozenset(("--after-context", "--before-context", "--context", "--regexp", "--file", "--glob",
                        "--iglob", "--type", "--type-not", "--max-count", "--max-depth", "--maxdepth",
                        "--threads", "--encoding", "--max-columns", "--replace", "--sort", "--sortr",
                        "--max-filesize", "--context-separator")),
             frozenset(("--hidden", "--no-ignore", "--ignore-case", "--smart-case", "--case-sensitive",
                        "--fixed-strings", "--word-regexp", "--line-regexp", "--line-number",
                        "--no-line-number", "--files-with-matches", "--files-without-match", "--count",
                        "--count-matches", "--invert-match", "--only-matching", "--quiet", "--multiline",
                        "--multiline-dotall", "--pcre2", "--no-heading", "--heading", "--with-filename",
                        "--no-filename", "--json", "--vimgrep", "--text", "--null", "--column",
                        "--no-messages", "--trim", "--stats", "--follow", "--unrestricted", "--byte-offset",
                        "--pretty", "--help", "--version")),
             frozenset(("--color", "--colour")))


def _allowlisted_options(words, k, allow, operands):
    """Round 35: whether words[k:] are only options the allowlist names (a value option takes the next
    word, or its value after = or attached to a short letter) and, when operands is true, operands."""
    value_short, plain_short, value_long, plain_long, eq_long = allow
    while k < len(words):
        w = words[k]
        t = w.text
        if w.opaque:
            return False
        if t == "--":
            return operands or k + 1 == len(words)
        if t.startswith("--"):
            option, eq, _value = t.partition("=")
            if option in value_long:
                k += 1 if eq else 2
            elif not eq and option in plain_long:
                k += 1
            elif eq and option in eq_long:
                k += 1
            else:
                return False
            continue
        if t.startswith("-") and len(t) > 1:
            step = 1
            for idx, ch in enumerate(t[1:], 1):
                if ch in value_short:
                    step = 1 if t[idx + 1:] else 2
                    break
                if ch not in plain_short and not (ch.isdigit() and words[0].text in ("grep", "rg")):
                    return False
            k += step
            continue
        if not operands:
            return False
        k += 1
    return True


def _allowlisted_command(command, tokens, ctx, spans):
    """Round 35 (qanorm34 N2): whether the whole command is one simple command of an allowlisted form:
    git [-C DIR] [--no-pager|-P] commit with the options _GIT_COMMIT_ALLOW names; gh pr or issue create,
    edit or comment with the options _GH_ALLOW names; grep or rg with the options _GREP_ALLOW or _RG_ALLOW
    names; with the command word exactly git, gh, grep or rg, no NAME=VALUE word, no $, backquote, <( or
    >( outside the exempt text (so no command, process, variable, parameter or arithmetic expansion), no
    operator (no pipeline, list, subshell, group or background), no redirection except the exempt
    here-document that git commit -F - or gh --body-file - reads, and no second command."""
    if _ALLOWLIST_EXPANSION.search(_blank_spans(command, spans)):
        return False
    span_set = set(spans)
    end = len(tokens)
    while end and tokens[end - 1][0] == "nl":
        end -= 1
    words = []
    heredocs = 0
    k = 0
    while k < end:
        kind, value = tokens[k]
        if kind == "w":
            words.append(value)
            k += 1
            continue
        if (kind == "op" and value in ("<<", "<<-") and not heredocs and k + 1 < end and tokens[k + 1][0] == "w"
                and any(rec is tokens and index == k and (start, stop) in span_set
                        for rec, index, _text, start, stop, _plain in ctx.heredocs)):
            heredocs += 1
            k += 2
            continue
        return False
    if not words or words[0].raw not in _EXEMPT_COMMAND_NAMES or _is_assignment(words[0].raw):
        return False
    name = words[0].raw
    if name == "git":
        k = 1
        while k < len(words) and words[k].text != "commit":
            if words[k].opaque or not words[k].text.startswith("-"):
                return False
            if words[k].text == "-C":
                k += 2
            elif words[k].text in ("-P", "--no-pager"):
                k += 1
            else:
                return False
        return k < len(words) and _allowlisted_options(words, k + 1, _GIT_COMMIT_ALLOW, True)
    if name == "gh":
        return (len(words) > 2 and words[1].text in ("pr", "issue") and words[2].text in _GH_ALLOW_SUBCOMMANDS
                and _allowlisted_options(words, 3, _GH_ALLOW, True))
    return _allowlisted_options(words, 1, _GREP_ALLOW if name == "grep" else _RG_ALLOW, True)


def _blank_spans(command, spans):
    """The command text with each span replaced by one space."""
    pieces = []
    pos = 0
    for start, end in sorted(set(spans)):
        start = max(start, pos)
        if end <= start:
            continue
        pieces.append(command[pos:start])
        pieces.append(" ")
        pos = end
    pieces.append(command[pos:])
    return "".join(pieces)


def _broad_exempt_spans(command):
    """The (start, end) spans of the command text that the broad layer does not read: the exempt words of
    top-level git commit, gh pr or issue, grep and rg commands, and the body of a top-level here-document
    with a plain delimiter that git commit -F - or gh pr or issue -F - reads. Round 33: none when the
    text outside them holds the word PATH or defines a function named git, gh, grep or rg. Round 34:
    none when the text outside them binds PATH (_path_bound), sets git configuration, starts the git or
    gh editor or names the message file or hooks (_git_runs_setting, _gh_runs_editor, _GIT_RUN_SETTING),
    or runs a program that may run stored text (_text_runner). Round 35: none unless the whole command is
    one simple command of an allowlisted form (_allowlisted_command)."""
    ctx = _Ctx()
    try:
        tokens, _end = _lex(ctx, command, 0, False)
        argvs = _command_argvs(tokens)
        all_argvs = list(argvs)
        for token_list in ctx.subs:
            all_argvs.extend(_command_argvs(token_list))
    except ParseError:
        return []
    spans = []
    for argv in argvs:
        words = _exempt_command_words(argv, getattr(argv, "assigns", ()))
        exempt = []
        if _RULES["git commit message"]:
            exempt.extend(_git_commit_message_words(words)[0])
        if _RULES["gh body"]:
            exempt.extend(_gh_body_words(words)[0])
        if _RULES["grep or rg pattern"]:
            exempt.extend(_pattern_words(words))
        spans.extend(w.span for w in exempt if _exempt_ok(w, command))
    for rec_tokens, op_index, text, start, end, plain in ctx.heredocs:
        if rec_tokens is not tokens or text is not command or not plain:
            continue
        words = _exempt_command_words(_segment_words(tokens, op_index), ())
        if ((_RULES["git commit message"] and _git_commit_message_words(words)[1])
                or (_RULES["gh body"] and _gh_body_words(words)[1])):
            spans.append((start, end))
    if spans and _RULES["simple command allowlist"] and not _allowlisted_command(command, tokens, ctx, spans):
        return []
    if spans and (_RULES["exact command word"] or _RULES["function shadowing"]):
        outside = _blank_spans(command, spans)
        if _RULES["exact command word"] and _PATH_WORD.search(outside):
            return []
        if _RULES["function shadowing"] and _SHADOW_DEFINITION.search(_STRIP_QUOTING.sub("", outside)):
            return []
    if spans and _RULES["PATH binding"] and _path_bound(_blank_spans(command, spans), all_argvs):
        return []
    if spans and _RULES["git editor and configuration"]:
        if _GIT_RUN_SETTING.search(_STRIP_QUOTING.sub("", _blank_spans(command, spans).replace("\\\n", ""))):
            return []
        for argv in all_argvs:
            words = _without_assignments(argv)
            if words and not words[0].opaque and (
                    (words[0].text == "git" and _git_runs_setting(words))
                    or (words[0].text == "gh" and _gh_runs_editor(words))):
                return []
    if spans and _RULES["exempt text runner"]:
        span_set = set(spans)
        if any(_text_runner(argv, span_set) for argv in all_argvs):
            return []
    return spans


def _broad_refusal(command):
    """Round 32 (D-2385): the outer layer. Whether the command text, with the exempt spans blanked, holds
    a removal word or a round 15 removal form (git clean, git reset --hard and the like)."""
    text = _blank_spans(command, _broad_exempt_spans(command))
    return _has_removal_text(text) or _has_removal_form_text(text)


def _evaluate(command):
    _scan_budget[0] = _SCAN_BUDGET  # round 20: the unknown-command scan budget is per command
    result = _check_command_text(command, 0)
    if result is not None:
        return result
    # Round 32 (D-2385): every parser deny above is the inner layer; the broad text refusal is the outer
    return BROAD if _broad_refusal(command) else ALLOW


def decide_command(command):
    verdict = _evaluate(command)
    if verdict in (DENY, CANNOT_PARSE, BROAD) and not _DENY_LOGIC_ON:
        return ALLOW
    return verdict


def decide_payload(data):
    try:
        if not isinstance(data, dict):
            return MALFORMED
        tool_name = data.get("tool_name")
        if not isinstance(tool_name, str):
            return MALFORMED
        if tool_name != "Bash":
            return ALLOW
        tool_input = data.get("tool_input")
        if not isinstance(tool_input, dict):
            return MALFORMED
        command = tool_input.get("command")
        if not isinstance(command, str) or "\x00" in command:
            return MALFORMED
        return decide_command(command)
    except Exception:
        return ERROR


def decide_raw(raw):
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        # Round 52 (grc review of round 50): bytes that are not UTF-8 or not JSON are malformed input; any
        # other failure here (a nesting too deep to parse, for one) stays an internal error
        return MALFORMED
    except Exception:
        return ERROR
    return decide_payload(data)


def hook_output(decision):
    """The stdout object for a decision: None for an allow, else the repository hooks' deny shape."""
    if decision == ALLOW:
        return None
    reason = _REASONS.get(decision, _REASONS[ERROR])
    banner = _BANNERS.get(decision, _BANNERS[ERROR])
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                   "permissionDecision": "deny",
                                   "permissionDecisionReason": reason},
            "systemMessage": banner}


class _DeadlineExpired(Exception):
    pass


class _Deadline(object):
    def __init__(self, seconds):
        self.seconds = seconds
        self.previous = None

    def __enter__(self):
        def expire(signum, frame):
            raise _DeadlineExpired()
        self.previous = signal.signal(signal.SIGALRM, expire)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
        return self

    def __exit__(self, *exc_info):
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self.previous)
        return False


def _emit(decision):
    obj = hook_output(decision)
    if obj is None:
        return 0
    try:
        sys.stdout.write(json.dumps(obj) + "\n")
        sys.stdout.flush()
        return 0
    except BaseException:
        try:
            sys.stderr.write("no-remove-guard: could not write the deny decision; blocking with exit 2\n")
            sys.stderr.flush()
        except BaseException:
            pass
        # Exit now: a normal exit would flush the unwritten stdout again at shutdown, and that second
        # failure turns the exit status into 120.
        os._exit(2)


def main(argv):
    if argv == ["--self-test"]:
        return _self_test()
    decision = ERROR
    try:
        if argv:
            raise ValueError("unexpected arguments")
        with _Deadline(DEADLINE_SECONDS):
            raw = sys.stdin.buffer.read()
            decision = decide_raw(raw)
    except BaseException:
        decision = ERROR
    return _emit(decision)


# --- self-test ---------------------------------------------------------------------------------------

def _bash(command):
    return {"tool_name": "Bash", "tool_input": {"command": command}}


_DENY_CASES = (
    "rm -rf /tmp/x",
    "rmdir build",
    "unlink f.txt",
    "shred -u secret.txt",
    "find . -name '*.pyc' -delete",
    "find . -type f -exec rm {} \\;",
    "find . -execdir rm -f {} +",
    "find /tmp/x -exec sudo rm -f {} +",
    "ls && rm x",
    "false || rm x",
    "ls; rm x",
    "printf 'a\\n' | rm -f a",
    "(rm x)",
    "{ rm x; }",
    "if true; then rm x; fi",
    "if false; then :; else rmdir d; fi",
    "for f in a b; do rm \"$f\"; done",
    "while false; do unlink x; done",
    "until rm x; do :; done",
    "case a in a) rm x;; esac",
    "echo $(rm x)",
    "echo `rm x`",
    "echo \"$(rmdir d)\"",
    "diff <(rm x) y",
    "cat <<EOF\n$(rm x)\nEOF",
    "X=$(rm x)",
    "f() { rm x; }",
    "command rm x",
    "exec rm x",
    "env -i FOO=1 rm x",
    "env -u HOME -- rm x",
    "env -S 'rm -rf x'",
    "sudo -u root rm x",
    "sudo -- rm x",
    "doas -u root rm x",
    "nohup rm x &",
    "nice -n 10 rm x",
    "nice -10 rm x",
    "ionice -c 3 rm x",
    "timeout -s KILL 5 rm x",
    "timeout 5 find . -delete",
    "time rm x",
    "time -p rm x",
    "/usr/bin/time -v rm x",
    "stdbuf -o0 rm x",
    "find . -print0 | xargs -0 rm -f",
    "xargs -I{} rm {} < list",
    "sudo env nice -n 5 rm x",
    "/bin/rm x",
    "/usr/bin/rm x",
    "\\rm x",
    "\"rm\" x",
    "r'm' x",
    "$'\\x72m' x",
    "FOO=1 rm x",
    ">log rm x",
    "! rm x",
    "git status\nrm x",
    "python3 -c 'import os; os.remove(\"x\")'",
    "python -c 'import shutil; shutil.rmtree(\"d\")'",
    "python3 -c 'from pathlib import Path; Path(\"x\").unlink()'",
    "python3 -c 'import pathlib; pathlib.Path(\"d\").rmdir()'",
    "python3 -c 'import os as o; o.unlink(\"x\")'",
    "python3 -c 'import os; os.removedirs(\"a/b\")'",
    "python3 -c 'import os; os.rmdir(\"d\")'",
    "python3 -I -c 'from os import remove; remove(\"x\")'",
    "python3 -Ic 'import os; os.remove(\"x\")'",
    "sudo python3 -c 'import os; os.unlink(\"x\")'",
    "find . -exec python3 -c 'import os, sys; os.remove(sys.argv[1])' {} \\;",
    # a << or <<= inside arithmetic is a shift, not a here-document that hides the next line
    "(( x = 1 << 2 ))\nrm -rf /tmp/x",
    "(( n <<= 1 ))\nrm x",
    "for (( i = 1; i < 8; i <<= 1 )); do :; done\nrm x",
    "echo $[ 1 << 2 ]\nrm x",
    "((x = 1 << 2)) && rm x",
    # trap runs its action string later
    "trap 'rm -rf /tmp/x' EXIT",
    "trap -- 'rm x' INT TERM",
    "trap \"rm -rf $tmp\" EXIT",
    # more wrappers and removal programs
    "builtin command rm x",
    "busybox rm x",
    "srm x",
    "wipe x",
    "gio remove x",
    "fd -e tmp -x rm",
    "fd . -X rm -f",
    "python3 -c 'import os; getattr(os, \"remove\")(\"x\")'",
    # a line continuation inside an assignment name (qanorm2 N1)
    "X\\\n=1 rm -rf x",
    "F\\\nOO=1 rm x",
    # bash cuts a $'...' string at a NUL (qanorm2 N2)
    "$'rm\\0' -rf x",
    "rm$'\\0' -rf x",
    "$'rm\\x00zz' x",
    "$'rm\\c@' x",
    "$'rm\\u0000' x",
    "/bin/rm$'\\0' x",
    # round 5 (qanorm4 N1): after a redirection bash reads no reserved word, so these lines all run
    "2>/dev/null [[ -d build\nrm -rf build\necho ]]",
    "</dev/null [[ x\nrm -rf y\necho ]]",
    "</dev/null [[ x\nrm -rf y\n]]",
    "</dev/null [[ x\ntrue && rm -rf y\necho ]]",
    "<<<x [[ x\nrm -rf y\necho ]]",
    "</dev/null ! [[ x\nrm -rf y\necho ]]",
    # round 5 (qanorm4 N3, gemnorm4 BLOCKER): every fd exec option is judged
    "fd -e tmp -x echo {} \\; -x rm {}",
    "fd -X echo \\; -X rm",
    "fd -x true \\; -X rm -rf",
    # round 5 (qanorm4 N4): import-alias and star-import tracking
    "python3 -c 'import os as o, sys; o.remove(\"x\")'",
    "python3 -c 'from os import *; remove(\"x\")'",
    # round 6 (qanorm5 F1): bash keeps a # glued to a process substitution in the same word
    "cat <(true)#; rm -rf y",
    "echo >(true)#; rm -rf y",
    "cat <(true)# ; rm -rf y",
    # round 6 (qanorm5 F4): one row per detector entry that no other row needs
    "find . -ok rm {} \\;",
    "find . -okdir rm {} \\;",
    "fd -e tmp --exec rm",
    "fd . --exec-batch rm -f",
    "python3 -c 'import posix; posix.remove(\"x\")'",
    "python3 -c 'import nt; nt.remove(\"x\")'",
    "python3 -c 'from shutil import rmtree; rmtree(\"d\")'",
    # pathlib exports no such function (none in python 3.14.4); this pins the from-import rule as written
    "python3 -c 'from pathlib import *; unlink(\"x\")'",
    # the sudo VAR=value skip, for a word with = that is not a shell assignment name
    "sudo A-B=1 rm x",
    # round 7 (gemnorm6b): the value of a find option is skipped as that value, not read as an exec
    "find . -name -exec -exec rm -rf y \\;",
    "find . -name -exec -delete",
    "find . -name -exec -o -delete",
    "find . -fprintf out -exec -exec rm -rf y \\;",
    "find . -newermt -exec -exec rm -rf y \\;",
    # round 7 (qanorm6 N4): a suffixed python build
    "python3.13t -c 'import os; os.remove(\"x\")'",
    "python3.13d -c 'import os; os.remove(\"x\")'",
    # round 8 (qanorm7 R1): GNU find ends -exec and -execdir at + only right after a word holding {},
    # and -ok and -okdir only at ;, so this -fprintf is inside the first block and the later one runs
    "find . -exec echo + -fprintf ';' -exec rm -rf y \\;",
    "find . -exec true + -fprintf ';' -exec rm -rf y \\;",
    "find . -execdir echo + -fprintf ';' -delete",
    "find . -ok echo {} + -fprintf ';' -exec rm -rf y \\;",
    "find . -okdir echo {} + -fprintf ';' -exec rm -rf y \\;",
    # round 8 (qanorm7 R3): more python interpreter names
    "python3.13-dbg -c 'import os; os.remove(\"x\")'",
    "python3-dbg -c 'import os; os.remove(\"x\")'",
    "pypy3 -c 'import os; os.remove(\"x\")'",
    # round 9 (qanorm8 finding 2): one row per python detector that no other row isolates
    "python3 -c 'from posix import remove; remove(\"x\")'",
    "python3 -c '__import__(\"os\").remove(\"x\")'",
    "python3 -c 'import importlib; importlib.import_module(\"os\").remove(\"x\")'",
    # round 13 (qanorm12 finding 3): git rm -f or --force without --cached, after git options it knows
    "git rm -f x",
    "git rm -rf d",
    "git rm --force x",
    "git rm --forc x",
    "git rm x -f",
    "git -C repo rm -f x",
    "git -c core.quotepath=off --no-pager --git-dir=.git rm -f x",
    "sudo git rm -f x",
    "git rm --cached --no-cached -f x",
    # round 13: a function body is still checked when the function is named after a removal program
    "rm() { rm -rf x; }",
    # round 13 (qanorm12 finding 5): the python launcher py
    "py -c 'import os; os.remove(\"x\")'",
    "py -3 -c 'import shutil; shutil.rmtree(\"d\")'",
    # round 15 (grc 0850 HIGH 1): git clean except a dry run or help, after the git options it knows
    "git clean -fdx",
    "git clean -f",
    "git clean -d",
    "git -C repo clean -fdx",
    "git -c core.quotepath=off --no-pager clean -f",
    "git clean -n --no-dry-run -f",
    "git clean -e -n -f",
    "git clean --exclude -n -f",
    "git clean -n \"$d\"",
    "sudo git clean -fdx",
    "nohup git -C repo clean -f",
    # round 15 (grc 0850 HIGH 1): git worktree remove with -f or --force
    "git worktree remove --force wt",
    "git worktree remove -f wt",
    "git worktree remove --forc wt",
    "git -C repo worktree remove --force wt",
    "sudo git worktree remove -f wt",
    # round 15 (grc 0850 MEDIUM 1): a bash, sh, dash or zsh -c string is checked as a command
    "bash -c 'rm -rf x'",
    "sh -c \"rm -f x\"",
    "dash -c 'rm x'",
    "zsh -c 'rm x'",
    "/bin/sh -c 'rm x'",
    "sh -ec 'rm x'",
    "bash -lc 'rm x'",
    "bash -o pipefail -c 'rm x'",
    "bash --norc -c 'rm x'",
    "bash --rcfile f -c 'rm x'",
    "bash --init-file f -c 'rm x'",
    "bash -O extglob -c 'rm x'",
    "bash -c -- 'rm x'",
    "sh -c \"rm -f $f\"",
    "sh -c 'find . -delete'",
    "bash -c 'bash -c \"rm x\"'",
    "bash -c 'ls; git rm -f x'",
    "find . -exec sh -c 'rm \"$1\"' _ {} \\;",
    "find . -name z -exec bash -c 'rm -rf \"$@\"' _ {} +",
    "xargs -0 sh -c 'rm \"$@\"' _ < list",
    "sudo bash -c 'rm -rf x'",
    "env -i sh -c 'rm x'",
    # round 15 (grc 0850 LOW 1): a python -c program that runs a shell removal
    "python3 -c \"import subprocess; subprocess.run(['rm', '-rf', 'd'])\"",
    "python3 -c \"import os; os.system('rm -rf d')\"",
    "python3 -c \"import os; os.popen('rm x')\"",
    "python3 -c \"from subprocess import call; call('rm x', shell=True)\"",
    "sudo python3 -c \"import os; os.system('rm -rf d')\"",
    # round 15 (grc 0850 LOW 2): setsid, flock (its command form), taskset and uv run
    "setsid rm x",
    "setsid -f rm -rf x",
    "setsid --wait rm x",
    "nohup setsid rm x",
    "flock /tmp/lock rm x",
    "flock -n /tmp/lock rm -rf x",
    "flock -w 5 /tmp/lock rm x",
    "flock /tmp/lock -c 'rm -rf x'",
    "flock /tmp/lock --command 'rm x'",
    "sudo flock /tmp/lock rm x",
    "taskset 0x1 rm x",
    "taskset -c 0 rm x",
    "taskset -a -c 0-3 rm x",
    "nice taskset -c 0 rm x",
    "uv run rm x",
    "uv run -- rm x",
    "uv -q run rm x",
    "uv run python -c 'import os; os.remove(\"x\")'",
    "uv run --with requests python3 -c 'import os; os.remove(\"x\")'",
    "sudo uv run rm x",
    # round 15 (grc 0850 LOW 3): the rmdir and removedirs python names, read through getattr or a
    # from-import (each row fails when its entry alone is taken out of PY_REMOVE_NAMES)
    "python3 -c 'import os; getattr(os, \"rmdir\")(\"d\")'",
    "python3 -c 'import os; getattr(os, \"removedirs\")(\"a/b\")'",
    "python3 -c 'from os import rmdir; rmdir(\"d\")'",
    "python3 -c 'from os import removedirs; removedirs(\"a/b\")'",
    "sudo python3 -c 'import os; getattr(os, \"rmdir\")(\"d\")'",
    # round 15 (grc 0850 brief): git reset --hard, git stash -u or -a, git checkout -f of a path
    "git reset --hard",
    "git reset --har HEAD~1",
    "git -C repo reset --hard HEAD~1",
    "sudo git reset --hard",
    "git stash -u",
    "git stash -ku",
    "git -C repo stash -u",
    "git stash push --include-untracked",
    "git stash push -a",
    "git stash save --all",
    "git stash push -m msg -u",
    "timeout 5 git stash -u",
    "git checkout -f -- x",
    "git checkout --force main -- x",
    "git -C repo checkout -f -- .",
    "git checkout -f --pathspec-from-file=list",
    "sudo git checkout -f -- x",
    # round 15 (grc 0850 brief): perl -e or -E with unlink or rmtree
    "perl -e 'unlink \"x\"'",
    "perl -E 'unlink \"x\"'",
    "perl -le 'unlink \"x\"'",
    "perl -e'unlink \"x\"'",
    "perl -w -e 'unlink glob \"*.tmp\"'",
    "perl -MFile::Path=rmtree -e 'rmtree(\"d\")'",
    "perl -I lib -e 'unlink \"x\"'",
    "perl5.36 -e 'unlink \"x\"'",
    "sudo perl -e 'unlink \"x\"'",
    # round 15 (grc 0850 brief): rsync with --delete or --remove-source-files
    "rsync -a --delete src/ dst/",
    "rsync -a --delete-after src/ dst/",
    "rsync -a --del src/ dst/",
    "rsync -a --remove-source-files src/ dst/",
    "rsync -n -a --delete src/ dst/",
    "sudo rsync -a --delete src/ dst/",
    "nice rsync -a --delete-excluded src/ dst/",
    # round 15 (grc 0850 brief): cargo clean
    "cargo clean",
    "cargo clean --manifest-path x/Cargo.toml",
    "cargo +nightly clean",
    "cargo -v clean",
    "cargo --color never clean",
    "cargo --unknown-opt clean",
    "env cargo clean",
    "sudo cargo clean -p foo",
    # round 16 (qanorm15 B1): chrt, unshare, fakeroot, eatmydata, strace, ltrace, pipx run, poetry run
    "chrt -f 10 rm x",
    "chrt 0 rm x",
    "chrt --fifo 10 rm x",
    "chrt -b 0 git clean -fdx",
    "unshare rm x",
    "unshare -r rm x",
    "unshare --mount --fork rm -rf x",
    "unshare -r git reset --hard",
    "fakeroot rm x",
    "fakeroot -- rm x",
    "fakeroot -u git clean -fdx",
    "eatmydata rm x",
    "eatmydata -- rm -rf x",
    "eatmydata cargo clean",
    "strace rm x",
    "strace -f -o out rm x",
    "strace -f git reset --hard",
    "strace -e trace=unlink rm x",
    "ltrace rm x",
    "ltrace -o out rm x",
    "ltrace git stash -u",
    "pipx run rm x",
    "pipx run --spec foo rm x",
    "poetry run rm -rf x",
    "poetry -C proj run rm x",
    "poetry run python -c \"import os; os.system('rm x')\"",
    "poetry run git clean -fdx",
    "sudo chrt -f 10 rm x",
    "nice eatmydata rm x",
    "sudo unshare -r strace -f fakeroot rm x",
    "timeout 5 poetry run rm x",
    # round 16 (qanorm15 B2, MD1): ksh, mksh, ash, busybox ash, fish, tcsh (and ksh93, csh) and su -c
    "ksh -c 'rm x'",
    "/bin/ksh -c 'rm x'",
    "sudo ksh -c 'rm x'",
    "find . -exec ksh -c 'rm \"$1\"' _ {} \\;",
    "ksh93 -c 'rm x'",
    "mksh -c 'rm x'",
    "ash -c 'rm x'",
    "busybox ash -c 'rm x'",
    "fish -c 'rm x'",
    "fish --command='rm x'",
    "fish --command 'rm x'",
    "tcsh -c 'rm x'",
    "csh -c 'rm x'",
    "ksh -c 'git clean -fdx'",
    "su -c 'rm -rf x'",
    "su root -c 'rm -rf x'",
    "su - root -c 'rm x'",
    "su --command='rm x' root",
    "su --command 'rm x' root",
    "su -lc 'rm x'",
    "su -s /bin/bash -c 'rm x' root",
    "sudo su -c 'git clean -fdx'",
    "nohup su -c 'rm x'",
    "su \"$U\" -c 'git clean -fdx'",
    # round 16 (qanorm15 M1): git submodule foreach, git rebase --exec or -x, git bisect run, and the other
    # git subcommands with an option whose value git runs as a command
    "git submodule foreach git clean -fdx",
    "git submodule foreach --recursive 'git clean -ffdx'",
    "git submodule --quiet foreach rm -rf x",
    "git -C repo submodule foreach 'git reset --hard'",
    "git submodule foreach -- rm x",
    "git rebase --exec 'rm x' HEAD~3",
    "git rebase -x 'git clean -fdx' main",
    "git rebase --exec='rm x' main",
    "git rebase --exe 'git stash -u' main",
    "git rebase -i -x 'rm x' main",
    "git rebase -ix 'rm x' main",
    "git rebase -s ort -x 'cargo clean' main",
    "git bisect run rm x",
    "git bisect run sh -c 'rm x'",
    "git bisect run 'git clean -fdx'",
    "git filter-branch --tree-filter 'rm -f secret' HEAD",
    "git difftool -x rm HEAD",
    "git difftool --extcmd='rm -f' HEAD",
    "git clone -u 'rm -rf x; git-upload-pack' src dst",
    "git fetch --upload-pack='rm -rf x' origin",
    "git pull --upload-pack 'rm -rf x' origin",
    "git ls-remote --upload-pack='rm -rf x' origin",
    "git archive --exec='rm -rf x' --remote=origin HEAD",
    "git push --receive-pack='rm -rf x' origin",
    "git grep -O'rm -f' pattern",
    "git grep --open-files-in-pager='rm -f' pattern",
    "git send-email --to-cmd='rm x' p.patch",
    "sudo git rebase -x 'rm x' main",
    "nohup git bisect run rm x",
    "strace -f git submodule foreach git clean -fdx",
    # round 16 (qanorm15 M2): the python shell-call rule, the perl check and the shell -c check also read
    # the round 15 removal forms
    "python3 -c \"import os; os.system('git clean -fdx')\"",
    "python3 -c \"import subprocess; subprocess.run(['git','clean','-fdx'])\"",
    "python3 -c \"import os; os.system('git reset --hard')\"",
    "python3 -c \"import os; os.system('cargo clean')\"",
    "python3 -c \"import os; os.system('git stash -u')\"",
    "python3 -c \"import os; os.system('git checkout -f -- x')\"",
    "python3 -c \"import os; os.system('git switch -f main')\"",
    "python3 -c \"import os; os.popen('rsync -a --delete a/ b/')\"",
    "sudo python3 -c \"import os; os.system('git clean -fdx')\"",
    "perl -e 'system(\"git clean -fdx\")'",
    "perl -e 'system(\"rm -rf x\")'",
    "perl -e 'print `cargo clean`'",
    "perl -e 'qx{git reset --hard}'",
    "perl -e 'exec \"git\", \"stash\", \"-u\"'",
    "sudo perl -e 'system(\"rsync -a --delete a/ b/\")'",
    # round 16 (qanorm15 MN3): ipython, git switch -f or --discard-changes, git checkout -f of . or a path
    "ipython -c \"import os; os.remove('x')\"",
    "ipython3 -c 'import shutil; shutil.rmtree(\"d\")'",
    "sudo ipython -c \"import os; os.remove('x')\"",
    "git switch --discard-changes main",
    "git switch --discard main",
    "git switch -f main",
    "git switch --force main",
    "git switch -fc new",
    "git -C repo switch -f main",
    "sudo git switch --discard-changes main",
    "git checkout -f .",
    "git checkout -f ./src",
    "git checkout -f .gitignore",
    "git checkout -f src/",
    "git checkout --force main x",
    "git checkout -f HEAD src/a.py",
    "git checkout -f --orphan new main x",
    "sudo git checkout -f .",
    "eatmydata git checkout -f .",
    # round 17 (qanorm16 F1): IPython shell escapes and shell magics, checked as shell command strings
    "ipython -c '!git clean -fdx'",
    "ipython -c '!git reset --hard'",
    "ipython -c '!cargo clean'",
    "ipython -c '!git stash -u'",
    "ipython -c '!git checkout -f -- .'",
    "ipython -c '!rsync -a --delete a/ b/'",
    "ipython -c '!rm -rf x'",
    "ipython -c '!!git clean -fdx'",
    "ipython -c 'x = !git clean -fdx'",
    "ipython -c 'print(1)\n  !cargo clean'",
    "ipython -c '%sx git clean -fdx'",
    "ipython -c '%system git reset --hard'",
    "ipython -c '%%bash\ngit clean -fdx'",
    "ipython -c '%%sh\ngit reset --hard'",
    "ipython -c '%%script bash\ncargo clean'",
    "ipython3 -c 'get_ipython().run_cell_magic(\"bash\", \"\", \"git clean -fdx\")'",
    "sudo ipython -c '!git clean -fdx'",
    "env ipython3 -c '%%bash\ngit clean -fdx'",
    "nohup ipython -c '%sx cargo clean'",
    # round 17 (qanorm16 F2): jobs -x runs its command
    "jobs -x rm -rf x",
    "jobs -x git clean -fdx",
    "jobs -x -- rm x",
    "builtin jobs -x rm -rf x",
    "command jobs -x cargo clean",
    # round 17 (qanorm16 F3): git checkout -f of a glob or an operand built at run time
    "git checkout -f ./*",
    "git checkout -f *",
    "git checkout -f \"$F\"",
    "git checkout -f src/*.py",
    "git checkout -f '*.py'",
    "git checkout --force {a,b}.txt",
    "sudo git checkout -f *",
    "env git checkout -f \"$F\"",
    # round 17 (qanorm16 F4): fish -C and --init-command, also before or after -c or --command
    "fish -C 'rm x'",
    "fish -i -C 'rm x'",
    "fish -iC 'rm x'",
    "fish -C'rm x'",
    "fish --init-command='echo hi' -c 'rm x'",
    "fish -C 'echo hi' -c 'rm x'",
    "fish -c 'echo hi' -C 'git clean -fdx'",
    "fish --command 'echo hi' --init-command 'rm x'",
    "sudo fish -C 'git reset --hard'",
    "env fish --init-command 'cargo clean'",
    # round 17: the over-deny this adds (fish passes these words to the script)
    "fish script.fish -C 'rm x'",
    # round 17 (qanorm16 F5): within the depth cap a round 15 removal form still denies as such
    "sudo " * 31 + "git clean -fdx",
    # round 17 (qanorm16 F7): git --no-lazy-fetch is a git option it knows
    "git --no-lazy-fetch clean -fdx",
    "sudo git --no-lazy-fetch reset --hard",
    # round 18 (qanorm17 M1): a process substitution inside an array assignment
    "a=(<(rm y))", "a=(>(rm -rf y))", "declare -a a=(<(rm y))", "a=(x <(git clean -fdx))",
    "sudo bash -c 'a=(<(rm y))'", "env bash -c 'a=(x >(cargo clean))'",
    # round 18 (qanorm17 MD1): an ipython option whose value is the next word
    "ipython --profile foo -c '!rm -rf x'", "ipython --log-level 10 -c '!git clean -fdx'",
    "sudo ipython --profile foo -c '!rm -rf x'",
    # round 18 (qanorm17 MD2): git checkout -f with no operand, submodule deinit -f, read-tree -u --reset,
    # checkout-index -f
    "git checkout -f", "git checkout --force", "git checkout --forc", "git submodule deinit -f sub",
    "git submodule deinit --all --force", "git submodule deinit --forc sub", "git read-tree -u --reset HEAD",
    "git read-tree --reset -u HEAD", "git checkout-index -f -a", "git checkout-index -af",
    "git checkout-index --force --all", "sudo git checkout -f", "env git submodule deinit -f sub",
    "nohup git read-tree -u --reset HEAD", "sudo git checkout-index -f -a",
    # round 18 (qanorm17 MD3): a shell -c string or interpreter program that runs its later arguments
    "sh -c '\"$@\"' sh rm -rf x", "bash -c '$0 $1 $2' rm -rf x", "find . -exec sh -c '\"$@\"' _ rm {} +",
    "perl -e 'system @ARGV' rm -rf x",
    "python3 -c 'import subprocess,sys; subprocess.run(sys.argv[1:])' rm -rf x",
    "bash -c '${1} \"$2\"' _ git clean", "sh -c '\"$@\"' _ git clean -fdx", "sudo sh -c '\"$@\"' sh rm -rf x",
    "env perl -e 'system @ARGV' cargo clean",
    "nohup python3 -c 'import os,sys; os.execvp(sys.argv[1], sys.argv[1:])' rm x",
    # round 18 (qanorm17 m1): an eval string, checked as a trap action is
    "eval 'git clean -fdx'", "builtin eval 'cargo clean'", "eval 'rm -rf x'", "sh -c 'eval rm x'",
    "sudo bash -c \"eval 'git reset --hard'\"", "eval git stash -u",
    # round 18 (qanorm17 m3): su and fish long option abbreviations
    "su --comm 'rm -rf x'", "su --com='git clean -fdx'", "su --sess 'rm x'", "fish --comm 'rm x'",
    "fish --init 'git clean -fdx'", "fish --ini='rm x'", "sudo su --comm 'rm -rf x'",
    "env fish --comm 'cargo clean'",
    # round 18 (qanorm17 m4): an ipython line that is the rm or rmdir shell alias
    "ipython -c 'rm *x'", "ipython -c 'rm -r*x'", "ipython -c 'print(1)\nrmdir d'", "ipython -c '%rm -rf x'",
    "sudo ipython -c 'rm *x'",
    # round 18 (qanorm17 m5): git checkout -f of pathspec magic or a tilde operand
    "git checkout -f ':(top)'", "git checkout -f ':/src'", "git checkout -f ~/x", "git checkout -f '~x'",
    "sudo git checkout -f ':(top)'", "env git checkout -f ~/x",
    # Round 19 (qanorm18 MEDIUM-1): the round 18 git discard forms in a python or perl shell call
    "python3 -c 'import os; os.system(\"git read-tree -u --reset HEAD\")'",
    "python3 -c 'import os; os.system(\"git checkout-index -f -a\")'",
    "python3 -c 'import os; os.system(\"git submodule deinit -f sub\")'",
    "python3 -c 'import subprocess; subprocess.run(\"git read-tree -u --reset HEAD\", shell=True)'",
    "sudo python3 -c 'import os; os.popen(\"git checkout-index --force -a\")'",
    "perl -e 'system(\"git read-tree -u --reset HEAD\")'", "perl -e 'system(\"git checkout-index -f -a\")'",
    "perl -e 'system(\"git submodule deinit -f sub\")'", "env perl -e 'system(\"git submodule deinit --force s\")'",
    # Round 19 (qanorm18 MEDIUM-3): later arguments run without naming "$@"
    "sh -c 'for a; do \"$a\" x; done' _ rm", "bash -c 'for a do $a x; done' _ rm",
    "sh -c 'for f\ndo $f x; done' _ rm", "bash -c 'select a; do $a x; done' _ rm",
    "sudo sh -c 'for a; do \"$a\" x; done' _ rm", "env bash -c 'for a do $a x; done' _ rm",
    "bash -c '${!#} x' _ rm", "bash -c '${BASH_ARGV[0]} x' _ rm", "nohup bash -c '${!#} x' _ rm",
    "python3 -c 'import os, sys; os.execvp(sys.orig_argv[3], sys.orig_argv[3:])' rm x",
    "sudo python3 -c 'import os, sys; os.execvp(sys.orig_argv[3], sys.orig_argv[3:])' rm x",
    "perl -e 'system(shift, shift)' rm x", "perl -e 'system(pop)' rm", "sudo perl -e 'system(shift, shift)' rm x",
    "ipython --c 'import os; os.remove(\"x\")'", "ipython --c='import os; os.remove(\"x\")'",
    "sudo ipython --c 'import os; os.remove(\"x\")'",
    # Round 20 (qanorm19 MINOR-1): ssh with a remote command
    "ssh host 'rm -rf /srv/x'", "sudo ssh host rm -rf /srv/x", "ssh -p 2222 host -- git clean -fdx",
    # Round 20 (qanorm19 MINOR-2): ipython code_to_run and exec_lines
    "ipython --InteractiveShellApp.code_to_run='!rm -rf x'",
    "ipython --TerminalIPythonApp.code_to_run='import os; os.remove(1)'",
    "ipython --InteractiveShellApp.exec_lines='[\"import shutil; shutil.rmtree(\\\"x\\\")\"]'",
    "ipython --InteractiveShellApp.code_to_run '!git clean -fdx'",
    "sudo ipython --InteractiveShellApp.code_to_run='!rm -rf x'",
    # Round 20 (qanorm19 MINOR-3): git checkout -f with --theirs or --ours
    "git checkout -f --theirs x", "git checkout -f --ours x", "git checkout --force --ours src/a.c",
    "git checkout -f -3 x", "env git checkout -f --theirs x",
    # Round 21 (qanorm20 F2): an unambiguous abbreviation of a known wrapper's long option
    "timeout --kill=1 5 git clean -fdx", "timeout --k 1 5 rm -rf x", "timeout --sig=KILL 5 git reset --hard",
    "sudo --us root git clean -fdx", "sudo --user=root --pres git stash -u", "env --un X git reset --hard",
    "env --ch /tmp git clean -f", "env --i git checkout -f -- x", "env --spl='git clean -fdx'",
    "nice --adj 5 cargo clean", "nice --adjust=5 rm -rf x", "ionice --cl 3 git clean -fdx",
    "stdbuf --out=L git clean -fdx", "xargs --max-a 1 rm < list", "setsid --fo git clean -fdx",
    "flock --ti 5 lockfile git clean -fdx", "chrt --fi 5 git clean -fdx", "unshare --fo git clean -fdx",
    "strace --fol git clean -fdx", "sudo --us root timeout --kill=1 5 git clean -fdx",
    "pipx run --spe pkg rm x",
    # Round 23 (qanorm22 F3): an unambiguous abbreviation of an rsync deleting long option
    "rsync -a --delet a/ b/", "rsync -a --dele a/ b/", "rsync -a --remov a/ b/", "rsync -a --remove a/ b/",
    "rsync -a --remove- a/ b/", "sudo rsync -a --delet a/ b/", "env rsync -av --dele src/ dst/",
    "sh -c 'rsync -a --delet a/ b/'",
    # Round 23 (qanorm22 F2): an os module bound to a new name, and a removal called through it
    "python3 -c \"import os; o = os; o.remove('x')\"", "python3 -c \"o = __import__('os'); o.remove('x')\"",
    "python3 -c \"import os; o = os; p = o; p.remove('x')\"",
    "python3 -c \"import os; print(o := os); o.remove('x')\"",
    "python3 -c \"import os; o, n = os, 1; o.remove('x')\"",
    "python3 -c \"import os; o = os; getattr(o, 'remove')('x')\"",
    "python3 -c \"import importlib; o = importlib.import_module('os'); o.remove('x')\"",
    "python3 -c \"import posix; o: object = posix; o.remove('x')\"",
    "python3 -c \"import os as m; o = m; o.remove('x')\"",
    "python3 -c \"import shutil; s = shutil; s.rmtree('x')\"",
    "python3 -c \"import pathlib; p = pathlib; p.Path('x').unlink()\"",
    # Round 24 (qanorm23 F1): an os, shutil or pathlib module reached through a walrus, either branch of
    # a conditional expression, or a tuple or list element indexed by an integer literal
    "python3 -c 'import os; (o := os).remove(\"x\")'",
    "python3 -c \"(o := __import__('os')).remove('x')\"",
    "python3 -c \"import os; getattr((o := os), 'remove')('x')\"",
    "python3 -c 'import os; (os if 1 else 0).remove(\"x\")'",
    "python3 -c 'import os; (0 if 1 else os).remove(\"x\")'",
    "python3 -c \"import os; o = os if True else None; o.remove('x')\"",
    "python3 -c \"import os; getattr(None if 0 else os, 'remove')('x')\"",
    "python3 -c 'import os; (os,)[0].remove(\"x\")'",
    "python3 -c \"import os; [0, os][1].remove('x')\"",
    "python3 -c \"import os; [0, os][-1].remove('x')\"",
    "python3 -c \"import os; o = (os,)[0]; o.remove('x')\"",
    "python3 -c \"import os; ((o := os) if 1 else 0,)[0].remove('x')\"",
    "python3 -c \"import shutil; (s := shutil).rmtree('x')\"",
    "python3 -c \"import shutil; (shutil if 1 else 0).rmtree('x')\"",
    "python3 -c \"import shutil; (shutil,)[0].rmtree('x')\"",
    "python3 -c \"import pathlib; (p := pathlib).Path('x').unlink()\"",
    "python3 -c \"import pathlib; (pathlib if 1 else 0).Path('x').rmdir()\"",
    "python3 -c \"import pathlib; [pathlib][0].Path('x').unlink()\"",
    # Round 25 (qanorm24 MINOR 1): an os, shutil or pathlib module reached through an operand of or and
    # and; the starred-element branch of a literal-indexed display (index 0 is os when xs is empty)
    "python3 -c \"import os; (os or 0).remove('x')\"",
    "python3 -c \"import os; (0 or os).remove('x')\"",
    "python3 -c \"import os; (1 and os).remove('x')\"",
    "python3 -c \"import os; o = os or None; o.remove('x')\"",
    "python3 -c \"import os; getattr(0 or os, 'remove')('x')\"",
    "python3 -c \"import shutil; (shutil or 0).rmtree('x')\"",
    "python3 -c \"import pathlib; (0 or pathlib).Path('x').unlink()\"",
    "python3 -c \"import os; xs = []; [*xs, os][0].remove('x')\"",
    # Round 25 (qanorm24 MINOR 2): operator.methodcaller with a literal removal name, as getattr with it
    "python3 -c \"import operator, os; operator.methodcaller('remove', 'x')(os)\"",
    "python3 -c \"from operator import methodcaller; import os; methodcaller('remove', 'x')(os)\"",
    "python3 -c \"import operator, os; o = os; operator.methodcaller('remove', 'x')(o)\"",
    "python3 -c \"import operator, os; operator.methodcaller('rmdir', 'd')(os)\"",
    "python3 -c \"import operator, shutil; operator.methodcaller('rmtree', 'x')(shutil)\"",
    "python3 -c \"import operator, pathlib; operator.methodcaller('unlink')(pathlib.Path('x'))\"",
    # Round 30 (qanorm29 F1): git submodule update -f or --force, with or without --checkout, as deinit -f
    "git submodule update -f", "git submodule update --force", "git submodule update --forc sub",
    "git submodule update -f --checkout", "git submodule update --checkout --force sub",
    "git submodule update --init -f", "git submodule update -Nf", "git submodule update --recursive --force",
    "git submodule --quiet update --force", "git -C repo submodule update -f", "sudo git submodule update --force",
    "env git submodule update -f --checkout sub", "bash -c 'git submodule update -f'",
    "git submodule foreach 'git submodule update -f'",
    "python3 -c 'import os; os.system(\"git submodule update -f\")'",
    "perl -e 'system(\"git submodule update --force --checkout\")'",
    # Round 31 (qanorm30 MINOR-1): git rebase --abort or --skip and git am --abort, as git reset --hard
    "git rebase --abort", "git rebase --skip", "git am --abort", "git rebase --abo", "git rebase --sk",
    "git am --abor", "git -C repo rebase --abort", "git -c core.quotepath=off am --abort",
    "sudo git rebase --skip", "env git am --abort", "nice git rebase --abort", "/usr/bin/git rebase --abort",
    "bash -c 'git rebase --abort'", "sh -c 'git am --abort'", "git submodule foreach 'git rebase --skip'",
    "python3 -c 'import os; os.system(\"git rebase --abort\")'",
    "perl -e 'system(\"git am --abort\")'",
    # Round 37 (grc round 36 LOW): git merge --abort and git cherry-pick --abort, read as git rebase --abort
    "git merge --abort", "git cherry-pick --abort", "git merge --abo", "git cherry-pick --ab",
    "git -C repo merge --abort", "sudo git cherry-pick --abort", "env git merge --abort",
    "bash -c 'git merge --abort'", "sh -c 'git cherry-pick --abort'",
    "python3 -c 'import os; os.system(\"git merge --abort\")'",
    "perl -e 'system(\"git cherry-pick --abort\")'",
    # Round 38 (qanorm37 F1): every --abort and --skip of rebase, am, merge, cherry-pick and revert
    "git revert --abort", "git revert --abo", "git revert --skip", "git revert --sk",
    "git cherry-pick --skip", "git cherry-pick --ski", "git am --skip", "git am --sk",
    "git -C repo revert --abort", "git -c core.quotepath=off cherry-pick --skip", "git --no-pager am --skip",
    "sudo git revert --skip", "env git am --skip", "/usr/bin/git revert --abort",
    "bash -c 'git revert --abort'", "sh -c 'git cherry-pick --skip'", "bash -c 'git am --skip'",
    "git submodule foreach 'git revert --abort'",
    "python3 -c 'import os; os.system(\"git revert --skip\")'",
    "perl -e 'system(\"git am --skip\")'",
    # Round 39 (qanorm38 F1): every stage-rewrite option of GIT_STAGE_REWRITE_OPTIONS with a named path,
    # in git checkout and git restore, as written, abbreviated, with = and in a short-option cluster
    "git checkout -m -- f", "git checkout -m f", "git checkout --merge -- f", "git checkout --merge f",
    "git checkout --m -- f", "git checkout --mer f", "git checkout -m main -- f", "git checkout -m .",
    "git checkout -m \"$F\"", "git checkout -qm -- f",
    "git checkout --conflict=merge f", "git checkout --conflict=diff3 -- f", "git checkout --conflict diff3 -- f",
    "git checkout --conflict=zdiff3 f", "git checkout --conf=diff3 -- f", "git checkout --c=merge -- f",
    "git checkout --ours -- f", "git checkout --theirs f", "git checkout --ou -- f", "git checkout --th f",
    "git checkout --ours x", "git checkout --theirs x", "git checkout -2 -- f", "git checkout -3 f",
    "git checkout -q3 f", "git checkout --ours --pathspec-from-file=list",
    "git restore -m f", "git restore --merge f", "git restore --m f", "git restore --merg -- f",
    "git restore --conflict=merge f", "git restore --conflict=zdiff3 f", "git restore --conflict diff3 f",
    "git restore --conf=diff3 -- f", "git restore --c=merge f",
    "git restore --ours f", "git restore --theirs f", "git restore --ou f", "git restore --t f",
    "git restore --th f", "git restore -2 f", "git restore -3 f", "git restore -Wm f", "git restore -W3 f",
    "git restore -s HEAD --ours f", "git restore --source HEAD -m f", "git restore -U 3 --theirs f",
    "git restore --ours -- f", "git restore --theirs \"$F\"", "git restore --ours .",
    "git restore --theirs --pathspec-from-file=list", "git restore --merge --no-merge f",
    "git -C repo restore --ours f", "sudo git restore --theirs f", "env git checkout --ours -- f",
    "/usr/bin/git restore -m f", "bash -c 'git restore --theirs f'", "sh -c 'git checkout -m -- f'",
    "git submodule foreach 'git checkout --ours -- f'",
    # Round 40 (qanorm39 F1): an abbreviated --pathspec-from-file= with a stage-rewrite option in checkout
    "git checkout -m --pathspec-fr=list", "git checkout -m --pathspec-from=list",
    "git checkout --merge --pathspec-from-fil=list", "git checkout --merge --pathspec-from-f=-",
    "git checkout --conflict=diff3 --pathspec-fr=list", "git checkout --c=merge --pathspec-fro=list",
    # (round 43, qanorm42 N1 to N3: the round 40 to 42 rows of a git command behind xargs, gxargs, fd,
    # fdfind, parallel, sem, xe and rush with no path named are cannot-parse rows now)
    # Round 40 (qanorm39 F3): a named path from an operation ref
    "git checkout MERGE_HEAD -- f", "git checkout MERGE_HEAD f", "git checkout CHERRY_PICK_HEAD -- f",
    "git checkout REVERT_HEAD f", "git restore -s MERGE_HEAD f", "git restore --source=MERGE_HEAD f",
    "git restore --so=CHERRY_PICK_HEAD f", "git restore -sMERGE_HEAD f", "git restore -Ws MERGE_HEAD f",
    "git restore --source=AUTO_MERGE -- f",
    # Round 41 (qanorm40 N1, N8): find puts the path where {} is, so the argv check denies
    "find . -execdir git restore --ours {} +",
    # (round 42, qanorm41 F3: the round 41 rows without {} are allow rows now, as find appends nothing)
    "find . -name '*.c' -exec git restore --theirs {} ';'", "find . -ok git checkout MERGE_HEAD {} ';'",
    # Round 41 (qanorm40 N4): worktree spellings, FETCH_HEAD, letter case, and any operand position
    "git checkout main-worktree/MERGE_HEAD -- f", "git checkout worktrees/wt1/MERGE_HEAD -- f",
    "git restore -s main-worktree/MERGE_HEAD f", "git checkout FETCH_HEAD -- f", "git restore -s FETCH_HEAD f",
    "git checkout merge_head -- f", "git checkout $OPT MERGE_HEAD -- f", "git checkout \"$OPT\" REVERT_HEAD f",
    # Round 41 (qanorm40 N7): every word after --end-of-options is an operand
    "git restore --ours --end-of-options -weird", "git restore -m --end-of-options -weird",
    "git checkout -m --end-of-options -weird", "git checkout --end-of-options MERGE_HEAD -- f",
    "git checkout -f --end-of-options -weird",
    # Round 42 (qanorm41 F5): gfind and bfs are read as find
    "gfind . -delete", "bfs . -delete", "bfs . -rm", "gfind . -name '*.c' -exec git restore --theirs {} +",
    "bfs . -exec rm {} ';'",
    # Round 43 (qanorm42 N2): an operation ref on the left of the merge-base form A...B
    "git checkout MERGE_HEAD...HEAD -- f", "git checkout MERGE_HEAD... -- f",
    "git restore -s MERGE_HEAD...HEAD f", "git restore --source=MERGE_HEAD... f",
    # Round 46: the qanorm45 probes the guard denies
    "env -S'git restore --ours' f",
    "find . -name '*.c' -exec env '-Sgit restore --ours' {} +",
)

_CANNOT_PARSE_CASES = (
    "echo 'unbalanced ; rm x",
    "python3 -c 'import os; os.remove('",
    "sudo --unknown-flag rm x",
    # a here-document that never meets its delimiter line, or whose delimiter holds an expansion
    "cat <<EOF\nrm x",
    "cat <<${X}\n${X}\nrm x\n${...}",
    "cat <<\"${X}\"\n${X}\nrm x\n${...}",
    "cat <<$(true)\n$(true)\nrm x\n$(...)",
    "cat <<${X}\n${X}\nrm -rf /tmp/x",
    # an escaped removal word in a command the lexer cannot parse
    "for f in a; { r\\m -f x; }",
    "for f in a; { $'\\x72m' -f x; }",
    "x=$(case a in a) echo hi;; esac)\nr\\m -f x",
    # env -S expands ${NAME}
    "env -S 'r${NRG_NOPE}m -rf x'",
    # constructs the lexer cannot read exactly, next to a removal word (qanorm2 N3 to N10, N13)
    "((echo '))' ) ; rm -rf x ) ; echo \\'",
    "echo $((echo '))' ; rm -rf x ) ) ; echo \\'",
    "(( '))' + $(rm -rf x) )) ; echo \\'",
    "echo $[ ']' + $(rm -rf x) ] \\'",
    "cat <<EOF\nE\\\nOF\nrm -rf x\nEOF",
    "a=( x # (\n)\nrm -rf y\n#)",
    "env -S 'rm\\_-rf\\_x'",
    "env -S 'rm\\cz' x",
    "a[x y]=1 rm z",
    "a[']']=1 rm z",
    "a[x;y]=1 rm z",
    "shopt -s expand_aliases\nalias del=rm\ndel -rf x",
    "hash -p /bin/rm zz; zz -rf x",
    "printf 'a\\n' | { mapfile -c 1 -C 'rm -f' arr; }",
    "readarray -C 'rm -f' -c 1 arr < list",
    "for f in a; { r$\"\"m -f x; }",
    "for f in a; { r$'\\0'm -f x; }",
    "fd --exec=rm",
    "fd -xrm",
    "fd --exec-batch=rm -f",
    # round 4 (qanorm3): a removal word beside a construct the guard does not model
    "echo ${ rm -rf x; }",
    "${ rm -rf x; }",
    "echo ${| rm -rf x; }",
    "echo \"${ rm -rf x; }\"",
    "v=${ rm -rf x; }",
    "echo ${\trm -rf x; }",
    "echo ${\nrm -rf x\n}",
    "rm$'\\400' -rf x",
    "echo $\"hi\"; git rm x",
    "env -S 'rm -rf x --' -S true",
    "env --split-string='rm -rf x' -S true",
    "BASH_CMDS[zz]=/bin/rm; zz -rf x",
    "shopt -s expand_aliases\nBASH_ALIASES[del]=rm\ndel -rf x",
    "declare -A BASH_CMDS=([zz]=/bin/rm); zz -rf x",
    "eval \"$(echo rm) -rf x\"",  # round 18: eval 'rm -rf x' is a deny row now (qanorm17 m1)
    "trap \"$(echo rm) -rf x\" EXIT",
    "let 'a[$(rm -rf x)]=1'",
    "bind -x '\"\\C-x\": rm -rf x'",
    "complete -C 'rm -rf x' foo",
    "compgen -C 'rm -rf x' foo",
    "fc -s ls=rm",
    "enable -f ./zz.so rm",
    # round 5 (qanorm4 N1): a time option other than -p; case after a redirection
    "time -x [[ a\nrm -rf y\necho ]]",
    "</dev/null case x in\nrm -rf y\necho ) :;; esac",
    # round 5 (qanorm4 N5): a command word built at run time beside a removal word
    "$SUDO rm -rf y",
    "$(echo rm) -rf y",
    # round 6 (qanorm5 F2): a brace-expanded command word is built at run time
    "{rm,-rf,y}",
    "{rm,} -rf y",
    "{,rm} -rf y",
    "echo ok; {rm,-rf,y}",
    "sudo {rm,-rf,y}",
    "rm{,} -rf y",
    # round 6 (qanorm5 F4): a repeated env --split-string, which only the env -S test catches
    "env --split-string='rm -rf y' --split-string='echo x'",
    # round 7 (gemnorm6b): fd may read a value that starts with - as an exec option, and an option the
    # guard does not know may take a value, so it cannot tell whether a later exec word starts a block
    "fd -e -x -x rm -rf y",
    "fd --unknown-opt -x -x rm -rf y",
    "find . -unknown-opt -exec -exec rm -rf y \\;",
    # round 7 (qanorm6 N1): a substitution command word behind a wrapper
    "sudo $(which rm) -rf y",
    "env $(which rm) -rf y",
    "nohup $(which rm) -rf y",
    "command $(which rm) -rf y",
    "exec $(which rm) -rf y",
    "nice $(which rm) -rf y",
    "stdbuf -o0 $(which rm) -rf y",
    "xargs $(which rm) < list",
    "sudo `which rm` -rf y",
    "sudo \"$(command -v rm)\" -rf y",
    # round 7 (qanorm6 N3): a digit flag before an attached fd exec option
    "fd -0x rm",
    "fd -1x rm",
    # round 8 (qanorm7 R1): an expansion in a find exec block may become ;, {} or several words
    "find . -exec echo $E + -fprintf ';' -exec rm -rf y \\;",
    "find . -exec echo $E -exec rm -rf y \\;",
    # round 8 (qanorm7 R2): an unquoted expansion in a find option value may become no word
    "find . -printf $E -printf -exec rm -rf y \\;",
    # round 9 (qanorm8 finding 1): such a value may also shift a later -delete into primary position
    "find . -printf $E -printf -delete",
    "find . -printf {,} -printf -delete",
    "find . -newermt $E -printf -delete",
    "find . -fprintf $F $E -printf -delete",
    # round 9 (qanorm8 finding 2): rows that only the env -S backslash check and the continuation-inside-
    # word check catch (env -S reads \_ as a separator, so this runs rm -rf y; the raw text holds no
    # removal word until \_ is read as one)
    "env -S '\\_rm\\_-rf\\_y'",
    "git rm -r --cached x\\\n  y",
    # round 10 (qanorm9 F1): a here-document opened in a substitution that closes on the same line; bash
    # reads its body from the later lines, so a quote there hid a later line from this lexer
    "echo $(cat <<EOF)\n'\nEOF\nrm -rf y\n#'",
    "cat <(cat <<EOF)\n'\nEOF\nrm -rf y\n#'",
    "echo \"$(cat <<EOF)\"\n'\nEOF\nrm -rf y\n#'",
    "echo $(cat <<EOF)\n'\nEOF\nfind / -delete\n#'",
    "echo $(cat <<EOF)\nrm x\nEOF",
    # round 10: the same here-document in each other construct the lexer leaves before its body is read
    "echo >(cat <<EOF)\n'\nEOF\nrm -rf y\n#'",
    "echo $(( $(cat <<EOF) ))\n'\nEOF\nrm -rf y\n#'",
    "(( $(cat <<EOF) ))\n'\nEOF\nrm -rf y\n#'",
    "echo $[ $(cat <<EOF) ]\n'\nEOF\nrm -rf y\n#'",
    "for (( i = $(cat <<EOF); i < 1; i++ )); do :; done\n'\nEOF\nrm -rf y\n#'",
    "echo ${x:-$(cat <<EOF)}\n'\nEOF\nrm -rf y\n#'",
    "a=($(cat <<EOF))\n'\nEOF\nrm -rf y\n#'",
    "echo $(echo $(cat <<EOF))\n'\nEOF\nrm -rf y\n#'",
    "echo $( (cat <<EOF) )\n'\nEOF\nrm -rf y\n#'",
    "cat <<A\n$(cat <<EOF)\nA\n'\nEOF\nrm -rf y\n#'",
    "echo `cat <<EOF`\n'\nEOF\nrm -rf y\n#'",
    "echo `cat <<EOF`\nrm -rf y\nEOF",
    # round 11 (qanorm10 F1): bash ends a here-document opened in a substitution at a delimiter line that
    # also carries the closing ), and runs the later lines
    "echo $(cat <<true\nhi\ntrue)\n( rm -rf y\ntrue\n)",
    "cat <(cat <<true\nhi\ntrue)\n( rm -rf y\ntrue\n)",
    "echo \"$(cat <<true\nhi\ntrue)\"\n( rm -rf y\ntrue\n)\n#\"",
    "echo $(cat <<true\nhi\ntrue)\n( find / -delete\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue)\n( python3 -c 'import os; os.remove(\"x\")'\ntrue\n)",
    "echo $(cat <<-true\n\thi\n\ttrue)\n( rm -rf y\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue )\n( rm -rf y\ntrue\n)",
    # round 11: a here-string with a removal word anywhere; round 32 (D-2384): a here-document whose body
    # holds a removal command in command position (round 32 moved the python -c program fed by a
    # here-document, the git commit message here-document and the rows whose removal word is outside
    # the body to _BROAD_CASES and _RULE_CASES)
    "cat <<'EOF'\nrm -rf /\nEOF",
    "cat <<EOF\nrm -rf x\nEOF",
    "cat <<-EOF\n\trm x\n\tEOF",
    "cat <<< 'rm x'",
    "x=$(cat <<EOF\nrm -rf y\nEOF\n)",
    "echo `cat <<EOF\nrm x\nEOF\n`",
    # round 12 (qanorm11 F1): on a line the round-11 shape hides, a python -c call the python check matches
    # although the text holds no removal word (adjacent literals, an escape, or a letter NFKC folds)
    "echo $(cat <<true\nhi\ntrue)\n( python3 -c 'import os; getattr(os, \"re\" \"move\")(\"x\")'\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue)\n( python3 -c 'import os; getattr(os, \"\\x72emove\")(\"x\")'\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue)\n( python3 -c 'import os; os.\uff52emove(\"x\")'\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue)\n( python3 -c 'import os; os.\uff52\uff4d\uff44\uff49\uff52(\"d\")'\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue)\n( python3 -c 'from pathlib import Path; getattr(Path(\"x\"), \"un\" \"link\")()'\n"
    "true\n)",
    "cat <(cat <<true\nhi\ntrue)\n( python3 -c 'import os; getattr(os, \"re\" \"move\")(\"x\")'\ntrue\n)",
    "cat <(cat <<true\nhi\ntrue)\n( python3 -c 'import os; getattr(os, \"\\x72emove\")(\"x\")'\ntrue\n)",
    "echo \"$(cat <<true\nhi\ntrue)\"\n( python3 -c 'import os; getattr(os, \"re\" \"move\")(\"x\")'\ntrue\n)\n#\"",
    "echo $(cat <<-true\n\thi\n\ttrue)\n( python3 -c 'import os; getattr(os, \"re\" \"move\")(\"x\")'\ntrue\n)",
    "echo $(cat <<true\nhi\ntrue )\n( python3 -c 'import os; getattr(os, \"re\" \"move\")(\"x\")'\ntrue\n)",
    # round 13 (qanorm12 finding 3): an expansion before -- may become -f; an unknown git option may take
    # the next word as its value; a subcommand built at run time
    "git rm \"$f\"",
    "git rm $(git ls-files -d)",
    "git --html-path rm -f x",
    "git $OPTS rm -f x",
    "git \"$(echo rm)\" -f x",
    # round 14 (qanorm13 F1): in a backquote inside double quotes bash reads \" as ", so a quote hid rm
    "echo \"`echo \\\"'\\\" ; rm y ; echo \\\"'\\\"`\"",
    "echo \"Result: `printf \\\"it's\\\"; rm -f t.txt; printf \\\" it's\\\"`\"",
    "echo \"a $(echo \"`echo \\\"'\\\" ; rm y ; echo \\\"'\\\"`\")\"",
    "echo \"`\\\"r\\\"m x`\"",
    # round 14 (qanorm13 F2, gemnorm12b item 8): a $' it cannot decode no longer stops the decoding, and
    # a "$'" in double quotes no longer hides a later split word
    "$'\\U00110000'; r\\m x",
    "echo $'\\U00110000'; r\\m -rf x",
    "echo $'\\U00110000'\n'r'm -rf x",
    "for f in a; { echo \"$'\"; r\\m -rf x; }",
    "x=$(case a in a) echo hi;; esac); echo \"$'\"; r\\m -rf x",
    "$'\\U00110000'; $'\\x72'm x",
    "for f in a; { echo \"$'\"; r\\m -rf x; echo \"'\"; }",
    # round 14 (qanorm13 F3): a python -c program ast cannot parse uses the full removal-word test
    "pypy -c 'import os; getattr(os, \"re\" \"move\")(\"x\"); print \"done\"'",
    "python2 -c 'import os; getattr(os, \"\\x72emove\")(\"x\"); print \"done\"'",
    "python3 -c 'import os; os.\uff52\uff45\uff4d\uff4f\uff56\uff45(\"x\"); print \"x\"'",
    # round 15 (grc 0850 MEDIUM 1): a -c string it cannot read, or an expansion that may become -c or the
    # string, next to a removal word
    "bash -c \"echo 'unbalanced ; rm x\"",
    "sh -c 'eval \"$C\" rm x'",  # round 18: sh -c 'eval rm x' is a deny row now (qanorm17 m1)
    "bash $OPTS 'rm x'",
    "bash -c $X 'rm x'",
    "sudo sh -c \"echo 'unbalanced ; rm x\"",
    "flock /tmp/lock -c \"echo 'unbalanced ; rm x\"",
    # round 15: an expansion that may become -f in git worktree remove
    "git worktree remove \"$wt\"",
    "sudo git worktree remove \"$wt\"",
    # round 15: an option it does not know, in perl and in uv run, next to a removal word
    "perl -Q -e 'unlink \"x\"'",
    "uv run --unknown-flag rm x",
    "sudo uv run --unknown-flag rm x",
    # round 16 (qanorm15 B1): a removal command name, or git and a removal subcommand form, after a command
    # word the guard does not know (a wrapper it does not know)
    "chroot /srv rm -rf x",
    "watch -n 1 rm x",
    "parallel rm ::: a b",
    "unbuffer rm x",
    "foo /bin/rm x",
    "foo git clean -fdx",
    "foo git rebase -x 'rm x' main",
    "sudo foo rm x",
    "find . -exec foo rm {} \\;",
    "toybox rm -rf x",
    # round 16: the over-deny this adds (nothing below removes a file)
    "grep rm file",
    "grep -r unlink src",
    "docker rm container",
    "find . -exec grep -l rm {} +",
    "ls | grep rm",
    "find . -maxdepth 1 -type f -exec grep -l rm {} +",
    "find . -exec grep -l rm {} + -fprintf out '%p\\n'",
    "find . -exec grep -l rm x{}y + -o -print",
    "find . -ok grep -l rm {} \\; -o -print",
    "find . -name \"$PAT\" -exec grep -l rm {} +",
    "which rm",
    "man rm",
    "npm rm lodash",
    "grep git clean",
    "foo git rm x",
    # round 16 (qanorm15 B1): an option of a new wrapper the guard does not know, next to a removal word
    "strace --unknown-flag rm x",
    "pipx run --unknown-flag rm x",
    "poetry --unknown-flag run rm x",
    # round 16 (qanorm15 M2): a shell -c string it cannot read, holding a round 15 removal form
    "bash -c \"echo 'x; git clean -fdx\"",
    "ksh -c \"echo 'x; cargo clean\"",
    "su -c \"echo 'x; git reset --hard\"",
    "bash -c $X 'git clean -fdx'",
    "su $OPTS 'git clean -fdx'",
    "python3 -c 'import os; os.system(\"git clean -fdx\"); print \"x\"'",
    # round 16 (qanorm15 M1): a git subcommand built at run time after submodule or bisect
    "git submodule $SUB rm x",
    "git bisect $SUB git clean -fdx",
    # round 17 (qanorm16 F1): an ipython program ast cannot parse that holds a round 15 removal form
    # (sx is an IPython automagic), and the over-deny this adds
    "ipython -c 'sx git clean -fdx'",
    "sudo ipython -c 'sx git clean -fdx'",
    "ipython -c 'print(\"git clean\") ; %time 1'",
    # round 17 (qanorm16 F2, F4): an expansion that may become jobs -x, or a fish command option
    "jobs $OPT rm -rf x",
    "builtin jobs $OPT git clean -fdx",
    "fish $OPT 'rm x'",
    "sudo fish -C \"$X\" rm",
    # round 17 (qanorm16 F5): past the depth cap, a round 15 removal form denies as cannot-parse
    "sudo " * 40 + "git clean -fdx",
    "nice " * 40 + "cargo clean",
    "sudo " * 40 + "rsync -a --delete a/ b/",
    "sudo " * 40 + "rm x",
    # round 18 (qanorm17 M2): a program read from stdin in a pipeline, or from a process substitution, with
    # a removal word or round 15 removal form in that pipeline or substitution
    "echo 'rm -rf x' | bash", "ls *.tmp | sed 's/^/rm /' | sh", "git ls-files -o | sed 's/^/rm -f /' | bash",
    "printf 'rm %s\\n' a b | sh", "echo 'rm -rf x' | sudo bash", "echo 'rm x' | env -i sh -s",
    "bash <(echo 'rm x')", "sudo bash <(echo 'git clean -fdx')", "echo 'rm x' | at now", "echo 'rm x' | batch",
    "echo 'git clean -fdx' | sh -s", "echo 'cargo clean' | nohup bash",
    "echo 'import os; os.remove(\"x\")' | python3", "echo 'unlink \"x\"' | perl",
    "python3 <(echo 'import shutil; shutil.rmtree(\"d\")')", "perl <(echo 'unlink \"x\"')",
    "at -f <(echo rm x) now", "{ echo rm x; } | sh", "x=$(echo 'rm x' | sh)",
    # round 18 (qanorm17 MD2, MD3, m1): an expansion that may become -f, -u or --reset, the over-deny of
    # an argument read as a command, and an eval string with an expansion
    "git submodule deinit \"$S\" sub", "git read-tree -u $OPT HEAD", "sh -c 'echo \"$@\"' _ ls rm x",
    "eval \"$X\" git clean -fdx",
    # round 18 (qanorm17 m2): an expansion that may become -c before a round 15 removal form
    "bash $X 'git clean -fdx'", "fish $X 'git clean -fdx'", "sudo sh $X 'cargo clean'",
    "env fish $X 'git reset --hard'",
    # round 18 (qanorm17 m6): past the depth cap, getattr and NFKC folding count
    "sudo " * 40 + "python3 -c 'import os; getattr(os, \"re\" \"move\")(\"x\")'",
    "nice " * 40 + "python3 -c 'import os; os.ｒｅｍｏｖｅ(\"x\")'",
    # Round 19 (qanorm18 MAJOR-1): a pipe continued onto the next line feeds the program reader
    "echo rm x |\nsh", "echo rm x | # c\nsh", "ls | sed 's/^/rm /' |\nbash", "echo 'git clean -fdx' |\n  bash",
    "printf 'rm x' |\nsudo sh", "{ echo rm x; } |\nsh", "echo rm x |&\nsh", "echo rm x |\nat now",
    "echo 'import os; os.remove(\"x\")' |\npython3", "echo rm x |\n\nsh", "echo rm x |\n# c\nsudo -u u sh",
    "echo 'unlink \"x\"' |\nenv perl", "bash -c 'echo rm x |\nsh'",
    # Round 19 (qanorm18 MAJOR-2): a program redirected in, by here-string or file descriptor, or fed to a
    # reader inside an output process substitution, plain and through a wrapper
    "sh < <(echo rm x)", "bash 0< <(echo rm x)", "sudo bash < <(echo rm x)", "bash -s < <(echo rm x)",
    "python3 < <(echo 'import os; os.remove(\"x\")')", "perl < <(echo 'unlink \"x\"')",
    "at now < <(echo rm x)", "sh < <(git ls-files -d | sed 's/^/rm /')", "echo rm x > >(sh)",
    "echo rm x | tee >(sh)", "echo rm x > >(sudo bash)", "nohup env A=1 bash < <(echo rm x)",
    "timeout 5 python3 - < <(echo 'import os; os.remove(\"x\")')", "bash <<< 'git clean -fdx'",
    "exec 3< <(echo rm x); sh <&3", "exec 3< <(echo rm x); sh 0<&3", "sh < rm-list.sh",
    "{ sh; } < <(echo rm x)", "( sh ) < <(echo rm x)", "exec < <(echo rm x); sh",
    "coproc sh; echo rm x >&\"${COPROC[1]}\"", "echo rm x | bash -c 'sh'", "echo rm x | sudo sh -c 'cat | sh'",
    "echo 'git clean -fdx' | fish -c 'sh'",
    # Round 19 (qanorm18 MEDIUM-2): /dev/stdin, /dev/fd/N and source or . of a process substitution
    "echo rm x | bash /dev/stdin", "echo rm x | sh /dev/stdin",
    "echo 'import os; os.remove(\"x\")' | python3 /dev/stdin", "echo rm x | source /dev/stdin",
    "source <(echo rm x)", ". <(echo rm x)", "echo rm x | bash /dev/fd/0", "bash /dev/fd/3 3< <(echo rm x)",
    "echo rm x | bash /proc/self/fd/0", "echo rm x | sudo bash /dev/stdin", "echo rm x | . /dev/stdin",
    "echo rm x | source /dev/fd/0", "builtin source <(echo rm x)", "command . <(echo 'git clean -fdx')",
    "source -- <(echo rm x)", "at -f /dev/stdin now < <(echo rm x)", "sudo at -f <(echo rm x) now",
    # Round 19 (qanorm18 MEDIUM-1): the round 18 git discard forms past the depth cap, in a shell -c string
    # it cannot parse and in a program read from stdin
    "sudo " * 40 + "git read-tree -u --reset HEAD", "sudo " * 40 + "git checkout-index -f -a",
    "sudo " * 40 + "git submodule deinit -f sub", "nice " * 40 + "git checkout-index --force -a",
    "bash -c 'git read-tree -u --reset HEAD; ('", "bash -c 'git checkout-index -f -a; ('",
    "bash -c 'git submodule deinit -f sub; ('", "echo 'git read-tree -u --reset HEAD' | sh",
    "echo 'git checkout-index -f -a' | sh", "echo 'git submodule deinit -f sub' | sudo sh",
    "echo 'git clean -fdx' | sh; (",
    # Round 20 (gemnorm19 BLOCKER): a cannot-parse from the argv check of passed-on arguments propagates
    "sh -c '\"$@\"' _ fd -xrm", "sudo sh -c '\"$@\"' _ fd -xrm", "bash -c '\"$@\"' _ fd --exec=rm",
    "env bash -c '\"$@\"' _ fd --exec=rm",
    "python3 -c 'import os,sys; os.execvp(sys.argv[1], sys.argv[1:])' fd -xrm",
    "nice python3 -c 'import os,sys; os.execvp(sys.argv[1], sys.argv[1:])' fd -xrm",
    "perl -e 'exec @ARGV' fd -xrm", "timeout 5 perl -e 'exec @ARGV' fd -xrm",
    # Round 20 (qanorm19 MAJOR-1): su, sudo -s or -i and doas -s with no command read stdin
    "echo 'rm -rf x' | sudo -s", "echo 'rm -rf x' | sudo -i", "echo 'rm -rf x' | sudo -u bob -s",
    "echo 'rm -rf x' | sudo --login", "echo 'rm -rf x' | sudo su", "echo 'rm -rf x' | sudo su -",
    "echo 'rm -rf x' | doas -s", "echo 'rm -rf x' | doas -u bob -s", "echo 'rm -rf x' | su",
    "echo 'rm -rf x' | su -", "echo 'rm -rf x' | su root", "echo 'rm -rf x' | su -l bob",
    "echo 'rm -rf x' | su -s /bin/bash bob", "echo 'rm -rf x' | exec su", "echo 'rm -rf x' | nohup sudo -s",
    "echo 'rm -rf x' | env su -", "echo 'git clean -fdx' | su -", "echo 'rm x' | su -c 'cat | sh' bob",
    "sudo -i < <(echo rm -rf x)", "sudo -s < <(echo 'git clean -fdx')", "su root < <(echo rm -rf x)",
    "timeout 9 su root < <(echo rm -rf x)",
    # Round 20 (qanorm19 MEDIUM-1): a later word, quoted or not, with a removal word or form
    "sh -c '$1' _ 'rm -rf x'", "bash -c '$0' 'rm -rf x'", "sh -c 'eval \"$1\"' _ 'rm -rf x'",
    "bash -c 'eval \"$@\"' _ 'rm -rf x'", "sh -c '$1' _ 'git clean -fdx'", "sh -c '$1' _ 'cargo clean'",
    "sudo sh -c '$1' _ 'rm x'", "find . -exec sh -c 'eval \"$1\"' _ 'rm -rf {}' \\;",
    "python3 -c 'import os,sys; os.system(sys.argv[1])' 'rm -rf x'",
    "env python3 -c 'import os,sys; os.system(sys.argv[1])' 'rm -rf x'",
    "python3 -c 'import subprocess,sys; subprocess.run(sys.argv[1], shell=True)' 'rm -rf x'",
    "perl -e 'system($ARGV[0])' 'rm -rf x'", "perl -e 'system shift' 'rm -rf x'",
    "nice perl -e 'system shift' 'rm -rf x'", "perl -e 'system @ARGV' 'rm -rf x'",
    "sh -c 'echo \"$1\"' _ 'remove me'",
    # Round 20 (qanorm19 MEDIUM-2): a script written and run in the same command
    "echo 'rm -rf build' > c.sh && bash c.sh", "printf 'rm -rf x\\n' > /tmp/c.sh; sh /tmp/c.sh",
    "echo rm -rf x > c.sh; chmod +x c.sh; ./c.sh", "echo 'rm x' > c.sh; nohup ./c.sh",
    "echo rm x | tee c.sh; sh c.sh", "echo 'rm x' | sudo tee c.sh; sh c.sh",
    "echo 'git clean -fdx' > c.sh && bash c.sh", "echo 'rm -rf x' > c.sh && sudo bash c.sh",
    "echo rm x >> c.sh; source c.sh", "echo rm x > c.sh; . ./c.sh",
    "echo 'import os; os.remove(\"x\")' > t.py && python3 t.py",
    "python3 build.py > out.log && git commit -m 'remove x'",
    # Round 20 (qanorm19 MINOR-1): a shell, interpreter, find or known wrapper after an unknown command;
    # ssh, awk and sed as program readers
    "chroot /srv sh -c 'rm -rf x'", "sudo chroot /srv sh -c 'rm -rf x'", "watch sh -c 'rm x'",
    "systemd-run --user sh -c 'git clean -fdx'",
    "chroot /srv python3 -c 'import shutil; shutil.rmtree(\"x\")'", "chroot /srv perl -e 'unlink \"x\"'",
    "echo 'rm -rf x' | chroot /srv sh", "echo 'rm -rf x' | runuser -u bob -- sh",
    "echo 'rm -rf x' | sudo runuser -u bob -- sh", "unknowncmd find . -delete", "watch find . -delete",
    "watch -n 5 sudo find /tmp/x -delete", "docker exec c sh -c 'rm /tmp/x'",
    "echo 'rm -rf x' | ssh host", "echo 'rm -rf x' | ssh host sh", "echo 'rm x' | ssh host 'cat | sh'",
    "cat rm-notes.txt | ssh host",
    "awk 'BEGIN{system(\"rm -rf x\")}'", "env awk 'BEGIN{system(\"rm -rf x\")}'",
    "gawk '{print | \"rm \" $1}' list", "awk '{ \"git clean -n\" | getline x }' f",
    "echo 'BEGIN{system(\"rm x\")}' | awk -f -", "awk '/remove|delete/' f",
    "sed -n '1e rm x' f", "sed 's/.*/rm &/e' list", "sudo sed -e '1e rm -rf x' f",
    "sed --expression='e rm x' f",
    # Round 21 (qanorm20 F1): awk -v values, operands after the program and NAME=VALUE words before awk
    # are program text when the program runs a command
    "awk -v cmd='rm x' 'BEGIN{system(cmd)}'", "awk -v c=rm 'BEGIN{system(c \" -rf x\")}'",
    "awk -vc='rm x' 'BEGIN{system(c)}'", "gawk --assign=c='rm x' 'BEGIN{system(c)}'",
    "awk 'BEGIN{system(ARGV[1])}' 'rm -rf x'", "awk 'BEGIN{system(c)}' c='git clean -fdx'",
    "gawk -e 'BEGIN{system(ARGV[1])}' 'rm x'", "C='rm x' awk 'BEGIN{system(ENVIRON[\"C\"])}'",
    "C='cargo clean' mawk 'BEGIN{system(ENVIRON[\"C\"])}'",
    "awk -v c='rm x' 'BEGIN{c | getline l; print l}'", "awk -v c='rm x' 'BEGIN{print \"y\" | c}'",
    "timeout 5 awk -v cmd='rm x' 'BEGIN{system(cmd)}'", "env C='rm x' awk 'BEGIN{system(ENVIRON[\"C\"])}'",
    "sudo C='rm x' nawk 'BEGIN{system(ENVIRON[\"C\"])}'", "C='rm x' env awk 'BEGIN{system(ENVIRON[\"C\"])}'",
    "C='rm x' timeout 5 awk 'BEGIN{system(ENVIRON[\"C\"])}'", "busybox awk 'BEGIN{system(ARGV[1])}' 'rm x'",
    "chroot /srv awk -v c='rm x' 'BEGIN{system(c)}'",
    # Round 21 (qanorm20 F3): git help.autocorrect, and a subcommand git does not ship with a removal word
    # or form in its argv
    "git -c help.autocorrect=immediate cleen -fdx", "git -c help.autoCorrect=1 rset --hard",
    "git --config-env=help.autocorrect=AC cleen -f", "git -c help.autocorrect=immediate status",
    "git config --global help.autocorrect immediate", "git config help.autocorrect 1",
    "git cleen rm -rf x", "git cleanup git clean -fdx", "git xyz --hard reset", "git ci -m 'remove x'",
    "sudo git -c help.autocorrect=1 cleen -fdx", "env git config help.autocorrect 1",
    "timeout 5 git cleen rm x", "watch git -c help.autocorrect=1 cleen -fdx",
    # Round 21 (qanorm20 F4): rows that fail when the enable, eval, hash, mawk or nawk entry is removed
    "enable -n echo; echo rm x", "eval true; echo rm x", "echo rm x; command eval true",
    "hash -p '/bin/rm' x; x y", "mawk 'BEGIN{system(\"rm x\")}'", "nawk 'BEGIN{system(\"rm x\")}'",
    "sudo mawk 'BEGIN{system(\"rm x\")}'", "timeout 5 nawk 'BEGIN{system(\"rm x\")}'",
    # Round 22 (qanorm21 N1): a round 15 removal form in a top-level command it cannot parse (a named
    # coproc, case inside $( ), an extglob pattern)
    "coproc NAME { echo hi; }; git clean -fdx", "coproc NAME { echo hi; }\ngit reset --hard",
    "coproc NAME { git reset --hard; }", "coproc NAME { git stash -u; }",
    "coproc NAME { git checkout -f -- .; }", "coproc NAME { cargo clean; }",
    "coproc NAME { while true; do git clean -fdx; done; }", "coproc NAME { if true; then git clean -fdx; fi; }",
    "x=$(case a in a) echo hi;; esac); git clean -fdx", "x=$(case a in a) echo hi;; esac)\ngit reset --hard",
    "x=$(case a in a) echo hi;; esac); git stash -u", "x=$(case a in a) echo hi;; esac); git checkout -f -- .",
    "shopt -s extglob; echo !(x); git clean -fdx", "shopt -s extglob; echo !(x)\ngit reset --hard",
    "shopt -s extglob; echo !(x); cargo clean",
    # Round 23 (qanorm22 F1): an unknown command word followed by a round 15 removal form other than a
    # removal command name (cargo clean, rsync with a deleting option, git clean, git reset --hard, git
    # stash -u, git checkout -f)
    "mywrap cargo clean", "chroot /srv cargo clean", "sudo chroot /srv cargo clean", "watch -n 5 cargo clean",
    "parallel cargo clean ::: a", "mywrap cargo +nightly clean", "mywrap cargo -q clean -p foo",
    "mywrap /usr/bin/cargo clean", "X=1 mywrap cargo clean", "nsenter -t 1 cargo clean",
    "mywrap rsync -a --delete a b", "chroot /srv rsync -a --remove-source-files a/ b/",
    "mywrap rsync -a --delete-after a/ b/", "mywrap rsync -a --del a/ b/", "mywrap rsync -a --delet a/ b/",
    "mywrap /usr/bin/rsync -a --delete a b", "watch rsync -a --delete a/ b/",
    "mywrap git clean -fdx", "chroot /srv git clean -f", "mywrap git reset --hard",
    "mywrap git stash -u", "mywrap git checkout -f -- x",
    "coproc NAME { rsync -a --delet a/ b/; }",
    # Round 25 (qanorm24 MEDIUM 1): a shell -c with no string operand behind xargs takes its string from
    # the input xargs reads
    "echo 'rm -rf x' | xargs -0 sh -c", "printf 'rm x' | xargs -0 bash -c",
    "echo 'git clean -fdx' | xargs -0 bash -c", "printf 'rm x\\n' | xargs -d '\\n' sh -c",
    "printf 'cargo clean' | xargs -0 sudo sh -c", "xargs -0 bash -ec < rm-cmds.txt",
    "printf 'rm x' | xargs -0 sh -c --", "printf 'rm x' | xargs -0 fish --command",
    # Round 26 (qanorm25 F1): a program operand that is missing or holds the xargs replace string, for a
    # shell, su or flock -c, python or ipython -c, perl -e, awk or sed, takes its program from the input
    "printf 'rm x' | xargs -0 -I{} sh -c '{}'", "printf 'git clean -fdx' | xargs -I{} sh -c '{}'",
    "echo 'rm -rf build' | xargs -I CMD sh -c CMD", "printf 'rm x' | xargs --replace sh -c '{}'",
    "printf 'rm x' | xargs -0 -i sh -c '{}'", "printf 'rm x' | xargs -0 -I % bash -c %",
    "printf 'rm x' | sudo xargs -0 -I{} sh -c '{}'",
    "printf 'rm x' | xargs -0 su -c", "printf 'rm x' | xargs -0 su root -c",
    "printf 'rm x' | xargs -0 su --command", "printf 'rm x' | xargs -0 flock /tmp/l -c",
    "printf 'import os; os.remove(1)' | xargs -0 python3 -c", "printf 'unlink 1' | xargs -0 perl -e",
    "printf '!rm x' | xargs -0 ipython -c", "printf 'BEGIN{system(\"rm x\")}' | xargs -0 awk",
    "printf 'e rm x' | xargs -0 sed -n", "printf 'import os; os.remove(1)' | xargs -0 -I{} python3 -c {}",
    "printf 'rm x' | xargs -0 -I{} flock /tmp/l -c '{}'", "printf 'rm x' | xargs -0 -I{} su -c '{}' root",
    "printf 'unlink 1' | xargs -0 perl -le", "printf 'e rm x' | xargs -0 -I@ sed -n @ f",
    "printf 'rm x' | xargs -0 --replace=@ bash -c 'echo @; @'",
    "printf 'import os; os.remove(1)' | xargs -0 python3 -I -c", "xargs -0 -I{} sh -c '{}' < rm-cmds.txt",
    # Round 27 (qanorm26 F1): a program behind xargs that runs its later arguments or a -v value
    "printf 'rm x' | xargs -0 sh -c '$0'", "printf 'rm\\0x' | xargs -0 sh -c '\"$@\"' _",
    "printf 'rm x' | xargs -0 bash -c 'eval \"$1\"' _", "printf 'rm x' | xargs -0 -I{} sh -c '$1' _ {}",
    "printf 'import os; os.remove(1)' | xargs -0 python3 -c 'import sys; exec(sys.argv[1])'",
    "printf 'unlink 1' | xargs -0 perl -e 'eval shift'", "printf 'rm x' | xargs -0 awk 'BEGIN{system(ARGV[1])}'",
    "printf 'rm x' | xargs -0 -I{} awk -v c='{}' 'BEGIN{system(c)}'",
    "printf 'rm x' | xargs -0 perl -e 'system @ARGV'",
    # Round 27 (qanorm26 F2): a replace string in other command-running forms, fish -C and --init-command
    # with a separate value, and perl -I DIR
    "printf 'rm x' | xargs -0 -I{} ssh host '{}'", "printf 'rm x' | xargs -0 -I{} git rebase -x '{}' main",
    "printf 'rm x' | xargs -0 -I{} git submodule foreach '{}'",
    "printf 'rm x' | xargs -0 -I{} git bisect run sh -c '{}'",
    "printf 'rm x' | xargs -0 -I{} find . -exec sh -c '{}' \\;", "printf 'rm x' | xargs -0 -I{} fd -x sh -c '{}'",
    "printf 'rm x' | xargs -0 -I{} uv run sh -c {}", "printf 'rm x' | xargs -0 -I{} fish -C '{}'",
    "printf 'rm x' | xargs -0 -I{} fish --init-command '{}'", "printf 'rm x' | xargs -0 -I{} perl -I lib -e '{}'",
    # Round 27 (qanorm26 F3): xargs -a or --arg-file reading a file the command writes
    "printf 'rm x' > c.txt; xargs -a c.txt -0 sh -c",
    "printf 'rm x' > c.txt; xargs --arg-file=c.txt -0 -I{} sh -c '{}'",
    "echo 'rm x' >> c.txt && xargs -0a c.txt -I{} bash -c '{}'",
    "printf 'import os; os.remove(1)' > p.txt; xargs -0 --arg-file p.txt python3 -c 'exec(input())'",
    # Round 27: the rest of the class, with any xargs options, wrappers on either side, and a program
    # word it does not know or one built at run time
    "printf 'rm x' | xargs -0 env", "printf 'rm x' | xargs sudo", "printf 'rm x' | xargs nice",
    "printf 'rm x' | xargs -0 timeout 5 sh -c '$0'", "printf 'rm x' | xargs -0 flock /tmp/l sh -c '$0'",
    "printf 'rm x' | xargs -0 -i su root -c 'eval \"{}\"'", "printf 'rm x' | xargs -0 --replace sh -c 'eval {}'",
    "printf 'rm x' | sudo xargs -0 env sh -c '$0'", "printf 'rm x' | xargs -0 chroot /srv sh -c '$0'",
    "printf 'rm x' | xargs -0 \"$SHELL\" -c '$0'", "printf 'git clean -fdx' | xargs -0 sh -c '$0'",
    "printf 'rm x' | xargs -0 -P 2 -n 1 ssh host", "printf 'rm x' | xargs -0 -I{} git -C repo rebase -x '{}' main",
    # Round 28 (qanorm27 N1): xargs -a or --arg-file in a command that writes any file, whatever the path
    "printf 'rm x' > /tmp/c.txt; cd /tmp; xargs -a c.txt sh -c",
    "cd /tmp; printf 'rm x' > c.txt; xargs -a /tmp/c.txt sh -c",
    "printf 'rm x' > c.txt; xargs -a ~/c.txt sh -c",
    "printf 'rm x' > c.txt; cp c.txt d.txt; xargs -a d.txt sh -c",
    "printf 'rm x' > c.txt; mv c.txt d.txt; xargs -a d.txt sh -c",
    "printf 'rm x' > c.txt; cd sub; xargs --arg-file=../c.txt -0 -I{} sh -c '{}'",
    "echo 'git clean -fdx' > c.txt; cp c.txt d.txt; xargs -0a d.txt bash -c",
    # Round 28 (qanorm27 N2): the round 27 class behind GNU parallel, sem, xe and rush
    "printf 'rm x' | parallel sh -c", "printf 'rm x' | parallel -j1 sh -c", "printf 'rm x' | parallel -0 sh -c",
    "printf 'rm x' | parallel -I{} sh -c '{}'", "printf 'git clean -fdx' | parallel sh -c",
    "printf 'git clean -fdx' | parallel -j1 sh -c", "parallel sh -c ::: 'rm x'",
    "parallel -j 2 bash -c ::: 'rm x'", "printf 'rm x' | sem sh -c", "printf 'rm x' | xe sh -c",
    "printf 'rm x' | rush 'sh -c {}'", "printf 'rm x' | rush '{}'", "printf 'rm x' | parallel",
    "parallel ::: 'rm x'", "printf 'rm x' | parallel 'sh -c'", "printf 'rm x' | parallel \"$SHELL\" -c",
    "printf 'rm x' | parallel chroot /srv sh -c", "printf 'rm x' | parallel env",
    "printf 'rm x' > c.txt; parallel -a c.txt sh -c", "printf 'rm x' > c.txt; parallel sh -c :::: c.txt",
    "printf 'rm x' | sudo parallel sh -c",
    # Round 29 (qanorm28 finding 1): a write under /dev/ other than /dev/null, /dev/zero, /dev/tty,
    # /dev/stdout and /dev/stderr counts as a written file
    "echo 'rm -rf x' > /dev/shm/c.sh; bash /dev/shm/c.sh",
    "echo 'rm -rf x' > /dev/shm/c.sh; chmod +x /dev/shm/c.sh; /dev/shm/c.sh",
    "echo 'rm -rf x' > /dev/mqueue/c.sh; sh /dev/mqueue/c.sh",
    "printf 'rm x' > /dev/shm/c.txt; xargs -a /dev/shm/c.txt -0 sh -c",
    "echo 'rm -rf x' | tee /dev/shm/c.sh; bash /dev/shm/c.sh",
    "printf 'rm x' > /dev/fd/3; xargs -a /dev/fd/3 -0 sh -c",
    # Round 29 (qanorm28 findings 2 and 6): cp, mv, install, ln and dd of= write a file
    "dd of=c.txt if=rm-cmds.txt; xargs -a c.txt -0 sh -c", "cp rm-cmds.txt c.txt; xargs -a c.txt -0 sh -c",
    "cp rm-all.sh c.sh; bash c.sh",
    "python3 -c \"open('c.sh','w').write('rm -rf x')\"; bash c.sh",
    "python3 -c \"open('c.txt','w').write('rm x')\"; xargs -a c.txt -0 sh -c",
    "perl -e 'open(F, \">c.sh\"); print F \"rm -rf x\"'; sh c.sh",
    # Round 29 (qanorm28 finding 6): a shell -c string that runs a reader, xargs or the written path
    "echo 'rm x' > c.sh; sh -c 'sh c.sh'", "printf 'rm x' > c.txt; sh -c 'xargs -a c.txt -0 sh -c'",
    "echo 'rm x' > c.sh; bash -c './c.sh'", "echo 'rm x' > c.sh; su -c '. ./c.sh'",
    # Round 29 (qanorm28 finding 3): xe -s with fed input or items from the command line
    "printf 'rm x' | xe -s '$1'", "printf 'git clean -fdx' | xe -s '$1'", "printf 'rm x' | xe -0s '$1'",
    "printf 'a\\n' | xe -s 'rm -rf \"$1\"'", "xe -s 'rm -rf \"$1\"' -a x",
    # Round 29 (qanorm28 line-178 MINOR): a replacement string as the command word
    "printf 'rm x' | parallel {}", "printf 'git clean -fdx' | parallel {}", "parallel {} ::: 'rm x'",
    "printf 'rm x' | parallel '{}'", "printf 'rm x' | parallel -I@ @",
    "printf 'rm x' | parallel --colsep ' ' {1} {2}", "printf 'rm x' | sem {}",
    "printf 'rm x' | parallel 'true; {}'", "printf 'rm x' | parallel '$SHELL -c'",
    # Round 29 (qanorm28 finding 4): quotes, backslashes and command substitution in a parallel command
    "printf 'rm x' | parallel '\"sh\" -c'", "printf 'rm x' | parallel 's\\h -c'",
    "printf 'rm x' | parallel '$(echo {})'", "printf 'rm x' | parallel '`echo {}`'",
    "printf 'rm x' | parallel 'echo $({})'",
    # Round 29 (qanorm28 finding 5): parallel with no command word after an option value
    "printf 'rm x' > c.txt; parallel -a c.txt", "printf 'rm x' > c.txt; parallel --arg-file c.txt",
    "printf 'rm x' > c.txt; parallel -j4 -a c.txt", "printf 'rm x' | parallel --joblog log",
    # Round 29 (qanorm28 MINOR 5): a quoted removal command name in a parallel, sem, xe or rush command
    "find . -name '*.tmp' | parallel 'rm {}'", "parallel \"rm -f\"", "ls | xe 'rm'",
    "parallel 'rm x' ::: a", "ls | rush 'rm {}'", "parallel 'git clean -fdx' ::: a",
    # Round 30 (qanorm29 F1): an expansion before -- that may become -f, and git submodule update -f fed
    # to a shell on stdin
    "git submodule update \"$OPT\" sub", "git submodule update --init $FLAGS",
    "echo 'git submodule update -f' | sh",
    # Round 31 (qanorm30 MINOR-1): git rebase --skip and git am --abort fed to a shell on stdin
    "echo 'git rebase --skip' | sh", "echo 'git am --abort' | bash",
    # Round 38 (qanorm37 F1): git revert --abort and git cherry-pick or am --skip fed to a shell on stdin
    "echo 'git revert --abort' | sh", "echo 'git cherry-pick --skip' | sh", "echo 'git am --skip' | bash",
    # Round 34 (qanorm33 N3): the round 33 function-shadowing rows, whose sh -c program an expansion supplies
    "git() { sh -c \"$3\"; }; git commit -m 'rm -rf x'",
    "function gh { sh -c \"$4\"; }; gh pr create --body 'rm -rf x'",
    "grep () { sh -c \"$2\"; }; grep -e 'rm -rf x' f",
    "rg() { sh -c \"$1\"; }; rg 'rm -rf x'",
    # Round 41 (qanorm40 N1): with parallel's ::: the unknown-command scan reads the items as git's paths
    "parallel -j4 git restore --theirs ::: a b",
    # Round 42 (qanorm41 F1): an option the PATH_APPENDERS table does not settle, an optional value, a
    # value that names git, or an expansion: every reading is checked, a finding denies as cannot-parse
    "ls | parallel --unknown-flag git restore --ours", "ls | parallel -Z git restore --ours",
    "ls | parallel -i git restore --ours", "ls | parallel --replace git restore --ours",
    "ls | parallel $OPTS git restore --ours", "ls | parallel --jobs git restore --ours",
    "ls | xe -Z git restore --ours", "ls | rush --zzz git restore --ours",
    "ls | xargs --zzz git restore --ours", "ls | gxargs -J % git restore --ours",
    # a shell line given as one word, and fd's attached and value-swallowed exec forms
    "ls | parallel 'git restore --ours'", "ls | parallel 'cd x && git checkout -m'",
    "ls | sem 'git checkout MERGE_HEAD'", "ls | rush 'git restore --ours'",
    "fd -e c --exec=git restore --theirs", "fd -e c -xgit restore --theirs", "fd -e -x git restore --theirs",
    # Round 43 (qanorm42 N1 to N3, N6): behind a program that puts paths or items into its command, a git
    # command whose subcommand removes or overwrites work denies as cannot-parse whatever the options
    # (_appended_git_check; round 45: every subcommand outside _GIT_APPENDED_ALLOWED). The round 40 to 42
    # deny rows of that kind:
    "git diff --name-only --diff-filter=U | xargs git restore --theirs", "xargs git restore --ours",
    "xargs git restore -m", "xargs -0 git restore --theirs", "xargs git checkout -m",
    "xargs git checkout --merge", "xargs git checkout --conflict=diff3",
    "git diff --name-only | xargs git checkout -m", "git diff --name-only | xargs git restore --ours --",
    "xargs sudo git restore --ours", "xargs git -C repo restore --ours", "xargs git restore -s MERGE_HEAD",
    "fd -e c -X git restore --theirs", "fd -e c -x git checkout -m", "fd -e c -x git checkout MERGE_HEAD",
    "fd -e c -X git restore -s MERGE_HEAD", "fd -e c --exec git checkout --conflict=merge",
    "fd -e c --exec-batch git restore --ours", "fdfind -e c -X git restore --theirs",
    "fd -e c -x sudo git restore --theirs", "ls | parallel git restore --ours",
    "ls | parallel git checkout -m", "ls | sem git restore --ours", "ls | xe git restore --ours",
    "ls | rush git restore --ours", "gxargs git restore --theirs", "git diff --name-only | gxargs -0 git checkout -m",
    "gxargs sudo git restore --ours",
    "ls | parallel -o git restore --ours", "ls | parallel --open-tty git restore --theirs",
    "ls | parallel --tty git checkout -m", "ls | parallel --silent git checkout -m",
    "ls | parallel -x git restore --theirs", "ls | parallel --resume git restore --ours",
    "ls | parallel -o git checkout MERGE_HEAD",
    "ls | sem -o git restore --ours", "ls | sem --silent git restore --ours",
    "timeout 5 parallel -o git restore --ours", "ls | parallel -j 4 --tag git restore --ours",
    "ls | parallel --sil git restore --ours", "ls | xe -N1 git restore --ours",
    "ls | rush -k git restore --ours",
    # (qanorm42 N1) a quoted parallel, sem or rush line that already names the path
    "ls | parallel 'git restore --ours {}'", "ls | parallel 'git restore --ours -- {}'",
    "ls | parallel 'git restore --ours' {}", "ls | parallel \"git restore --ours\" \"{}\"",
    "ls | sem 'git restore --ours {}'", "ls | rush 'git restore --ours {}'",
    "ls | rush -j 4 'git restore --ours {}'", "ls | parallel 'git checkout MERGE_HEAD -- {}'",
    "parallel 'git restore --ours {}' ::: a b", "ls | parallel 'cd x && git restore --ours {}'",
    "ls | parallel 'git restore --theirs {} ; echo done'",
    # (qanorm42 N3, N4) a value option or flag the table may misread, and rush flags after the command
    "ls | parallel -S host git restore --ours", "ls | parallel --sshlogin host git restore --ours",
    "ls | rush git restore -- --ours",
    # the round 42 residual forms: an expansion as the command word, a wrapper _inner_command does not
    # look past, an xe line in one quoted word, and an xe -s script
    "xargs $GIT restore --ours", "xargs flock /tmp/l git restore --ours",
    "fd -x flock /tmp/l git restore --ours", "ls | xe 'git restore --ours'",
    "ls | xe -s 'git restore --ours \"$1\"'",
    # over-refusals: the round 40 to 42 allow rows of a guarded subcommand with no path-rewriting option
    "git diff --name-only | xargs git restore", "fd -e c -X git restore --staged",
    "git diff --name-only | gxargs git restore", "ls | parallel git restore",
    # Round 44 (qanorm43 B1): a git value option's value that is not exactly one non-empty piece (an
    # empty word, or a word that holds a blank) is cannot-parse
    "ls | xargs git -C '' restore --ours", "ls | xargs git -C \"\" restore --ours",
    "git diff --name-only | xargs git -C '' checkout -m", "ls | xargs git -c 'a.b=1 log' restore --ours",
    "ls | xargs git -c 'a.b=1 log' checkout -m", "ls | xargs git --namespace 'x log' restore --ours",
    "ls | xargs git --namespace '' restore --ours", "ls | gxargs git -C '' restore --theirs",
    "fd -e c -X git -C '' restore --theirs", "fd -e c -x git -c 'a.b=1 log' checkout -m",
    "fdfind -e c -X git -C '' restore --ours", "ls | xe git -C '' restore --ours",
    "ls | parallel -q git -C '' restore --ours", "ls | parallel -q git -c 'a.b=1 log' restore --ours",
    "ls | parallel -q git -C '' checkout -m", "ls | sem -q git -c 'a.b=1 log' restore --theirs",
    "ls | rush -- git -C '' restore --ours", "ls | xargs sudo git -C '' restore --ours",
    "ls | xargs env git -c 'a.b=1 status' restore --ours", "ls | xargs git -C '' restore -s MERGE_HEAD",
    # (qanorm43 M1) a subcommand from the items the program reads or from a replacement string
    "(echo restore; echo --ours; git diff --name-only) | xargs git", "ls | xargs -I% git % --ours",
    "parallel git {} --ours f ::: status restore", "parallel git {1} --ours {2} ::: log restore ::: f",
    # Round 45 (qanorm44 F1, F2): behind a path-adding program, git is allowed only with a listed
    # subcommand (_GIT_APPENDED_ALLOWED) as the plain word right after git; git's options are not read.
    # (qanorm44 F1 a) an attached long-option value that holds a blank
    "ls | xargs git '--namespace=x log' restore --ours", "ls | xargs git \"--namespace=x log\" checkout -m",
    "ls | xargs git '--exec-path=/x log' restore --ours", "ls | xargs git '--work-tree=. log' restore --theirs",
    "ls | gxargs git '--namespace=x log' restore --ours", "fd -e c -X git '--namespace=x log' restore --ours",
    "fdfind -e c -x git '--namespace=x log' checkout -m", "ls | xe git '--namespace=x log' restore --ours",
    "ls | parallel -q git '--namespace=x log' restore --ours",
    "ls | sem -q git '--namespace=x log' restore --ours", "ls | rush -- git '--namespace=x log' restore --ours",
    "ls | xargs sudo git '--namespace=x log' restore --ours",
    "ls | xargs env git '--namespace=x status' restore --ours", "ls | xargs git '--git-dir=.git x' restore --ours",
    "ls | parallel \"git '--namespace=x log' restore --ours\"",
    "ls | xe -s 'git --namespace=\"x log\" restore --ours \"$@\"'",
    # (qanorm44 F1 b) a value that the shell line parallel, sem or rush builds joins with the next word
    "ls | parallel git --namespace 'x\\' log restore --ours", "ls | parallel git -c 'a.b=1\\' log restore --ours",
    "ls | parallel git --namespace \"'x\" \"log'\" restore --ours",
    "ls | parallel git -c \"'a.b=1\" \"log'\" restore --ours",
    "ls | sem git --namespace 'x\\' log restore --theirs", "ls | rush git --namespace 'x\\' log restore --ours",
    "ls | parallel git -C 'x\\' log checkout -m",
    # (qanorm44 F1 c) a quoted shell line whose quote counts balance
    "ls | parallel \"git --namespace \\\"'\\\"'x log' restore --ours\"",
    # (qanorm44 F2 a) bundled xargs replacement options
    "printf 'restore\\0' | xargs -0IR git R --ours f", "printf 'restore\\0' | xargs -0I R git R --ours f",
    "printf 'restore\\0' | xargs -rIR git R --ours f", "printf 'restore\\0' | xargs -0iR git R --ours f",
    "printf 'restore\\0' | gxargs -0IR git R --ours f",
    # (qanorm44 F2 b) GNU parallel input sources in the subcommand's place
    "parallel git :::: subs.txt ::: --ours ::: f", "(echo restore) | parallel git :::: - ::: --ours ::: f",
    "parallel -a subs.txt git ::: --ours ::: f", "parallel --arg-file subs.txt git ::: --ours",
    "parallel git ::::+ subs.txt ::: f",
    # a listed word that a replacement option may replace, an expansion before git, a quote or escape in
    # the subcommand word, an alias, and an option before the subcommand
    "printf 'restore\\0' | xargs -0Ilog git log --ours f", "ls | parallel --parens lg git log --ours",
    "ls | xargs $OPTS git log --ours", "ls | parallel git 'log' --ours", "ls | parallel git lo\\g --ours",
    "ls | xargs git co --ours", "ls | xargs git -c alias.x=restore x --ours",
    # over-refusals round 45 adds, as cannot-parse (moved from _ALLOW_CASES): a subcommand outside the
    # list, a replacement option before git, and git named in a quoted shell line
    "echo main | xargs -I{} git rebase -x 'make test' {}",
    "echo 'git status' | xargs -0 -I{} git submodule foreach '{}'",
    "echo test | xargs -I{} git bisect run sh -c 'make {}'", "git diff --name-only | xargs git add",
    "fd -e c -x git add", "find . -name '*.c' -exec git add {} +", "ls | parallel git add", "gxargs git add",
    "ls | parallel -o git add", "ls | parallel 'git add'", "ls | parallel 'git log --oneline {}'",
    "ls | parallel --unknown-flag git add", "ls | xargs --zzz git add", "fd -e c --exec=git add",
    "xargs sh -c 'git -C \"$d\" status'", "git log --format=%H | xargs git cherry-pick",
    "ls | xargs git -C repo log", "ls | xargs git --no-pager log", "ls | xargs -I{} git log {}",
    "ls | xargs git grep -l x", "fd -e c -X git commit -m x",
    # Round 46 (qanorm45 F1, F2, F4): behind a path-adding program, the command it runs must start with a
    # listed plain program (_appended_command_check, _APPENDED_PLAIN_PROGRAMS). Over-refusals round 46
    # adds, as cannot-parse (moved from _ALLOW_CASES): a shell, su, flock, python, ipython, perl, awk, sed,
    # ssh, find, fd, uv, fish, env, sudo, nice, timeout, gzip, make or a quoted shell line there
    'find . -exec sh -c \'wc -l "$1"\' _ {} \\;',
    "printf 'make all' | xargs -0 sh -c",
    "echo 'echo hi' | xargs sh -c",
    "printf 'ls -la' | xargs -d '\\n' bash -c",
    'find . -name \'*.txt\' -print0 | xargs -0 sh -c \'wc -l "$@"\' _',
    "ls | xargs -I{} sh -c 'echo {}'",
    "find . -name '*.md' | xargs -I % bash -c 'wc -l %'",
    "printf 'make all' | xargs -0 -I{} sh -c '{}'",
    'echo bob | xargs -I{} su -c whoami {}',
    'echo bob | xargs su -c id',
    "printf 'id' | xargs -0 su -c",
    "ls | xargs -I{} flock /tmp/l -c 'cat {}'",
    "printf 'make all' | xargs -0 flock /tmp/l -c",
    "printf '1 2' | xargs python3 -c 'import sys; print(sys.argv[1:])'",
    "printf 'print(1)' | xargs -0 python3 -c",
    "find . -name '*.py' -print0 | xargs -0 -I{} python3 -m py_compile {}",
    "printf 'x' | xargs -0 ipython -c 'print(1)'",
    "printf 'print(1)' | xargs -0 ipython -c",
    "ls | xargs perl -ne 'print if /TODO/'",
    "printf 'print 1' | xargs -0 perl -e",
    "ls *.txt | xargs awk '{print FILENAME}'",
    "printf 'BEGIN{print 1}' | xargs -0 awk",
    "ls *.txt | xargs sed -n '1p'",
    "printf 'p' | xargs -0 sed -n",
    "ls | xargs -I{} sed -n '1p' {}",
    "printf 'make all' | xargs -0 sh -c '$0'",
    'printf \'make\' | xargs -0 bash -c \'eval "$1"\' _',
    "printf 'print(1)' | xargs -0 python3 -c 'import sys; exec(sys.argv[1])'",
    "printf 'print 1' | xargs -0 perl -e 'eval shift'",
    "printf 'ls' | xargs -0 awk 'BEGIN{system(ARGV[1])}'",
    'echo host1 | xargs -I{} ssh {} uptime',
    "ls | xargs -I{} find {} -name '*.py' -exec wc -l {} +",
    'echo src | xargs -I{} fd -e py . {} -x wc -l',
    "printf 'pytest' | xargs -0 -I{} uv run sh -c {}",
    "printf 'echo hi' | xargs -0 -I{} fish -C '{}'",
    'echo /tmp/l | xargs -I{} flock {} make',
    'echo bob | xargs -I{} su {} -c id',
    "printf 'FOO=1' | xargs env",
    'ls | xargs sudo wc -l',
    'ls | xargs nice -n 5 wc -l',
    'ls | xargs timeout 5 wc -l',
    "printf 'make' > c.txt; xargs -a c.txt sh -c",
    "printf 'make' > c.txt; xargs --arg-file=c.txt -0 -I{} sh -c '{}'",
    'xargs -a files.txt -0 sh -c \'wc -l "$@"\' _',
    'xargs --arg-file=hosts.txt -I{} ssh {} uptime',
    'xargs -a cmds.txt sh -c; echo rm',
    "printf 'make' > c.txt; cp c.txt d.txt; xargs -a d.txt sh -c",
    'parallel gzip ::: a.log b.log',
    "parallel -j4 'echo {}' ::: a b c",
    "find . -name '*.py' | parallel -j 8 python3 -m py_compile {}",
    "seq 3 | parallel sh -c 'echo $0'",
    'cat hosts | parallel ssh {} uptime',
    'sem -j 2 make test',
    "ls | rush 'echo {}'",
    "printf 'make all' | parallel sh -c",
    "parallel sh -c ::: 'make all'",
    'ls | parallel -j 4 gzip {}',
    'ls | xargs sudo git status',
    # Round 46: the qanorm45 probes the guard refuses as cannot-parse (F1 env -S, F2 a PARALLEL setting
    # and mixed-case options, F4 a replacement string as the command word, F5 a GIT_ setting), the
    # review's comparison rows, and the round 46 forms next to them
    "ls | xargs env -S'git restore --ours'",
    "ls | xargs env '-Sgit restore --ours'",
    "ls | xargs env --split-string='git restore --ours'",
    "ls | xargs sudo env '-Sgit restore --ours'",
    "fd -e c -X env -S'git restore --theirs'",
    "fd -e c -X env '-Sgit checkout -m'",
    'ls | parallel env -S"\'git restore --ours\'"',
    "ls | xargs env -S 'git restore --ours'",
    "echo restore | PARALLEL='-I log' parallel git log --ours f",
    'ls | env PARALLEL=\'--rpl "log s/.*/restore/"\' parallel git log --ours',
    "export PARALLEL='-I log'; echo restore | parallel git log --ours f",
    'parallel -kI log git log --ours f',
    'echo restore | parallel --Replace=log git log --ours f',
    "ls | parallel --RPL 'log s/.*/restore/' git log --ours",
    'echo restore | sem --REPLACE=log git log --ours f',
    'echo git | xargs -I% % restore --ours f',
    'echo t | xargs -I% gi% restore --ours f',
    'echo t | parallel gi{} restore --ours f',
    "find /usr/bin -maxdepth 1 -name git -exec {} restore --ours f ';'",
    'parallel {} restore --ours f ::: git',
    'ls | xargs env GIT_EXTERNAL_DIFF=./fix.sh git diff',
    'ls | xargs env GIT_PAGER=./fix.sh git log',
    'ls | xargs env GIT_CONFIG_PARAMETERS="\'core.fsmonitor=./fix.sh\'" git status',
    "ls | xargs env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.fsmonitor 'GIT_CONFIG_VALUE_0=git restore --ours .' git status",
    'ls | xargs git -c core.fsmonitor=./fix.sh status',
    'ls | xargs git --namespace=x restore --ours',
    'ls | xargs git log\\ restore --ours',
    'ls | xargs git -- restore --ours',
    "ls | xargs git '' restore --ours",
    'ls | xargs env -u X git restore --ours',
    'ls | xargs sudo -u u git restore --ours',
    'ls | xargs nice git restore --ours',
    'ls | xargs git -c alias.rev-parse=status rev-parse',
    'ls | xargs -I gr grep x',
    'ls | xargs -Igr grep x',
    "ls | parallel grep x '{};' env -S'git restore --ours'",
    "ls | parallel grep '{= system(1) =}'",
    "ls | parallel --ssh 'sh -c' grep x",
    "ls | parallel -S 'env x' grep x",
    'PATH=./bin:/usr/bin; ls | xargs grep x',
    'ls | xargs sh -c \'grep x "$@"\' sh',
    "ls | xe -s 'grep x'",
    'ls | parallel -J prof grep x',
    # Round 51 (grc review of round 50): a patch here-document whose diff keeps a removal word on a context
    # line ( rm x;, with the leading space a diff writes): the here-document command-position rule reads
    # it as a removal command in command position, an over-refusal in the safe direction (see BROAD LAYER)
    "patch -p1 <<'EOF'\n--- a/build.sh\n+++ b/build.sh\n@@ -1,2 +1,2 @@\n rm x;\n-echo a;\n+echo b;\nEOF",
)

_ALLOW_CASES = (
    "echo rm -rf /",
    "printf '%s\\n' rm rmdir",
    # round 16: grep -r unlink src, docker rm container, find . -exec grep -l rm {} + and ls | grep rm are
    # cannot-parse rows now (a removal command name after a command word the guard does not know)
    "grep -r 'unlink' src",
    "echo \"rm x\"",
    "echo 'rm -rf x'",
    "ls # rm x",
    "git rm file.txt",
    "docker run --rm image",
    "ls -la",
    "command -v rm",
    "find . -name '*.py'",
    "find . -exec grep -l 'rm' {} +",
    "python3 -c 'xs = [1]; xs.remove(1)'",
    "python3 -c 'print(\"os.remove\")'",
    "python3 -c 'import os  # os.remove(x)'",
    "mkdir -p /tmp/grc/deleteme && mv x /tmp/grc/deleteme/",
    "echo $(echo rm)",
    "kubectl delete pod x",
    "rmate file",
    "",
    "ls | grep 'rm'",
    "[[ rm == x ]] && echo ok",
    "for rm in a b; do echo $rm; done",
    "xargs echo rm < list",
    "timeout 5 echo rm",
    "env FOO=rm ls",
    "sudo -l",
    "echo 'unbalanced",
    "echo rm > out.txt 2>&1",
    "case rm in rm) echo rm;; esac",
    "echo \"it's here\"",
    "(( x = 1 << 2 ))\necho done",
    "echo $[ 1 << 2 ]",
    "trap - EXIT",
    "trap 'echo done' EXIT",
    "trap -p",
    "rm --help",
    "python3 -c 'print(getattr([], \"remove\"))'",
    "gio info x",
    "fd -x echo rm",
    # the cannot-read checks leave these alone
    "docker run --rm \\\n  image",
    "git rm -r --cached x \\\n  y",
    "echo $((1 << 3)) rm",
    "for (( i = 0; i < 3; i++ )); do echo \"rm $i\"; done",
    "a[1]=x; echo rm",
    "a=(x y); echo rm",
    "env -S 'echo\\_hi'",
    "mapfile -t lines < list",
    "echo $'a\\0b'",
    "fd -e txt -x echo rm",
    # round 5 controls
    "2>/dev/null [[ -d build ]] && echo rm",
    "time -p [[ -d build ]] && echo rm",
    "fd -x echo {} \\; -x echo rm",
    "\"$EDITOR\" notes.txt",
    # round 6 controls: bash reads these as comments
    "cat <(true) #; rm -rf y",
    "((1))#; rm -rf y",
    # round 7 controls; find reads this -delete as the -name pattern, so nothing is removed
    "find . -maxdepth 1 -type f -exec grep -l 'rm' {} +",
    "find . -name -delete",
    "fd -H -e txt -x echo rm",
    "sudo $(which apt-get) install x",
    "python3.13t -c 'print(1)'",
    # round 8 controls
    "find . -exec grep -l 'rm' {} + -fprintf out '%p\\n'",
    "find . -exec grep -l 'rm' x{}y + -o -print",
    "find . -ok grep -l 'rm' {} \\; -o -print",
    "find . -name \"$PAT\" -exec grep -l 'rm' {} +",
    "find . -exec grep -l \"$PAT\" {} +",
    "pypy3 -c 'print(1)'",
    # round 9 controls: no -delete after the value, a quoted value, and a -delete that stays a value
    "find . -printf $E -printf x",
    "find . -printf {,} -print",
    "find . -newermt $E -print",
    "find . -printf \"$E\" -printf -delete",
    # round 10 control: a here-document left unread without a removal word
    "echo $(cat <<EOF)\nhello\nEOF",
    # round 11 controls: a here-document or here-string with no removal word anywhere stays allowed
    "cat <<'EOF'\nhello /\nEOF",
    "cat <<EOF\nhello $HOME\nEOF",
    "cat <<-EOF\n\thello\n\tEOF",
    "cat <<< 'hello'",
    "git commit -m \"$(cat <<'EOF'\nFix the parser\nEOF\n)\"",
    "x=$(cat <<EOF\nhello\nEOF\n)",
    "echo `cat <<EOF\nhello\nEOF\n`",
    "echo $(cat <<true\nhi\ntrue)\n( echo y\ntrue\n)",
    "cat <<true\nhi\ntrue)\n( echo y\ntrue\n)",
    # round 11 controls: a << that is not an operator (quoted, escaped, in a comment or arithmetic)
    # next to a removal word
    "echo \"a << b\"; git rm x",
    "echo 'a <<< b' && git rm x",
    "echo a\\<\\<b; git rm x",
    "ls # cat <<EOF\ngit rm x",
    "echo $(( 1 << 2 )); git rm x",
    # round 13 controls: git rm without -f, git rm --cached (index only), -f as a path after --, another
    # subcommand with -f, a function named after a removal program, and the py launcher without a removal
    "git -C repo rm -r d",
    "git rm --cached -f x",
    "git rm -r --cached --force d",
    "git rm -- -f",
    "git rm -- \"$f\"",
    "git checkout -f main",
    "rm() { echo nope; }",
    "rm () { echo nope; }",
    "py -c 'print(1)'",
    # round 14 controls (qanorm13 F1): the same body inside $( ) in double quotes, in a backquote outside
    # double quotes, and in a backquote inside ${...}; bash runs no rm for any of them
    "echo \"$(echo \\\"'\\\" ; rm y ; echo \\\"'\\\")\"",
    "echo `echo \\\"'\\\" ; rm y ; echo \\\"'\\\"`",
    "echo \"${x:-`echo \\\"'\\\" ; rm y ; echo \\\"'\\\"`}\"",
    # round 15 controls: a git clean dry run or help, git worktree remove without -f, git reset without
    # --hard, git stash without -u or -a (or with -u as a message), git checkout -f of a branch or a path
    # without -f, and other subcommands
    "git clean -n",
    "git clean --dry-run -d",
    "git clean -nfdx",
    "git -C repo clean -n -d",
    "git clean -n -- -f",
    "git clean -h",
    "git clean --help",
    "git help clean",
    "git worktree remove wt",
    "git worktree list",
    "git reset --soft HEAD~1",
    "git reset HEAD x",
    "git stash",
    "git stash pop",
    "git stash show -p",
    "git stash push -m -u x",
    "git checkout -f main",
    "git checkout -- x",
    "git checkout main -- x",
    # round 15 controls: a shell -c string with no removal, a script file, and words after the string
    "bash -c 'echo rm'",
    "sh -c 'ls -la'",
    "bash -c 'git rm x'",
    "bash script.sh",
    "sh -c 'echo hi' rm",
    "sudo bash -c 'echo rm'",
    # round 15 controls: python -c shell calls without a removal word
    "python3 -c \"import subprocess; subprocess.run(['ls'])\"",
    "python3 -c \"import os; os.system('ls')\"",
    # round 15 controls: wrappers that run nothing or no removal
    "setsid echo rm",
    "flock 9",
    "flock /tmp/lock echo rm",
    "flock -n /tmp/lock -c 'echo rm'",
    "taskset -p 0x1 1234",
    "taskset -c 0 echo rm",
    "uv run pytest",
    "uv run python -c 'print(1)'",
    "uv run -m pytest",
    "uv pip install rm",
    # round 15 controls: perl, rsync and cargo forms that remove nothing
    "perl -e 'print 1'",
    "perl -pi -e 's/a/b/' f",
    "perl script.pl unlink",
    "rsync -a src/ dst/",
    "rsync -a --delay-updates src/ dst/",
    "cargo build",
    "cargo clean --help",
    "cargo help clean",
    "cargo run -- clean",
    # round 16 controls (qanorm15): the new wrappers and runners with no removal, or running nothing
    "chrt -m",
    "chrt -p 1234",
    "chrt -f -p 10 1234 rm",
    "chrt -f 10 ls",
    "unshare -r ls",
    "fakeroot dpkg-deb -b pkg",
    "eatmydata apt-get install x",
    "strace -c ls",
    "strace -o out ls",
    "ltrace ls",
    "pipx run black .",
    "pipx install rm",
    "poetry run pytest",
    "poetry remove requests",
    "sudo strace -f echo rm",
    # round 16 controls: a command word the guard does not know, with a removal word that is quoted, part
    # of a longer word or no removal command name, and bash builtins that never run an operand
    "grep 'rm' file",
    "grep -e \"rm\" file",
    "tee rm.log",
    "sed -n /rm/p f",
    "kubectl delete pod x",
    "apt-get remove x",
    "pytest -k rm_test",
    "type rm",
    "help rm",
    "export rm=1",
    "test -f rm",
    "grep -r 'git clean' docs",
    "foo git status",
    # round 16 controls: other shells and su with no removal
    "ksh -c 'echo rm'",
    "fish -c 'ls'",
    "fish --command='echo rm'",
    "tcsh -c 'echo hi'",
    "su -c 'ls' root",
    "su - root",
    "su -s /bin/sh root",
    # round 16 controls: git subcommands that run a command with no removal
    "git submodule foreach git status",
    "git submodule foreach 'git pull'",
    "git submodule update --init",
    "git rebase -i HEAD~3",
    "git rebase --exec 'make test' main",
    "git rebase -x 'npm test' main",
    "git rebase -s ort main",
    "git bisect run make test",
    "git bisect start",
    "git difftool -x 'diff -u' HEAD",
    "git difftool -t meld HEAD",
    "git clone https://example.invalid/r.git",
    "git grep -O pattern",
    "git grep -e rm",
    "git push --delete origin x",
    # round 16 controls: python, perl and shell -c strings with no removal form
    "python3 -c \"import subprocess; subprocess.run(['git','status'])\"",
    "python3 -c \"import os; os.system('cargo build')\"",
    "python3 -c \"import os; os.system('git checkout main')\"",
    "perl -e 'system(\"ls\")'",
    "perl -e 'print `date`'",
    "bash -c \"echo 'x; git status\"",
    "ipython -c 'print(1)'",
    # round 16 controls (qanorm15 MN2, MN3): every git abbreviation of --dry-run, git switch without -f,
    # and git checkout -f of one word that may be a branch
    "git clean --d",
    "git clean --dr -fdx",
    "git clean --dry",
    "git clean --dry-",
    "git clean --dry-r",
    "git clean --dry-ru -d",
    "git switch main",
    "git switch -c new",
    "git switch -c f",
    "git switch -C feature",
    "git checkout -f -b new origin/main",
    "git checkout -f feature/x",
    "git checkout --orphan new",
    "git checkout -",
    # round 17 controls: forms that remove nothing
    "ipython -c '!ls -la'",
    "ipython -c '!!git status'",
    "ipython -c '%sx git status'",
    "ipython -c '%%bash\necho hi'",
    "ipython -c 'print(\"git clean\")'",
    "ipython -c 'print(\"!git status\")'",
    "sudo ipython -c '!git status'",
    "jobs",
    "jobs -l",
    "jobs -x echo rm",
    "builtin jobs -p",
    "git checkout main",
    "git checkout \"$BRANCH\"",
    "git checkout *.py",
    "git checkout -f HEAD~1",
    "sudo git checkout \"$BRANCH\"",
    "fish -C 'set -x A 1'",
    "fish -iC 'echo hi' -c 'ls'",
    "fish script.fish",
    "sudo fish -C 'echo hi'",
    "bash -C script.sh",
    "sudo " * 40 + "git status",
    "git --no-lazy-fetch status",
    "git --no-lazy-fetch clean -n",
    "sudo git --no-lazy-fetch log",
    # round 18 controls: forms that remove nothing
    "a=(<(ls y))", "a=(x y z)", "declare -a a=(<(git status))",
    "echo 'ls -la' | bash", "curl -fsSL https://example.invalid/i.sh | sh", "git ls-files | sh -s",
    "bash <(echo 'echo hi')", "echo 'print(1)' | python3", "echo 'rm x' | grep -c x",
    "echo 'echo hi' | at now", "bash -c 'ls' | grep x",
    "ipython --profile foo -c 'print(1)'", "ipython --profile foo script.py",
    "git submodule deinit sub", "git submodule deinit --all", "git read-tree HEAD", "git read-tree -m -u HEAD",
    "git read-tree --reset HEAD", "git checkout-index -a", "git checkout-index -u -a --prefix=out/",
    "git checkout -f main", "git checkout -",
    "sh -c '\"$@\"' _ ls -la", "bash -c 'echo $1' _ hello", "perl -e 'print @ARGV' a b",
    "python3 -c 'import sys; print(sys.argv)' a b",
    "eval 'git status'", "eval ls -la", "builtin eval 'cargo build'",
    "bash $X 'git status'", "fish $X 'ls'",
    "su --comm 'ls'", "fish --comm 'echo hi'", "su --sh /bin/bash user",
    "ipython -c 'rm = 3'", "ipython -c 'rmx = 3'", "ipython -c 'ls -la'",
    "git checkout ':(top)'", "git checkout ~/x",
    "sudo " * 40 + "python3 -c 'print(1)'",
    # Round 19 (qanorm18): forms of the new rules that remove nothing
    "echo hello |\nsh", "ls |\ngrep x", "sh < <(echo ls)", "sh <<< 'ls -la'", "echo ls > >(sh)",
    "echo ls | bash /dev/stdin", "source <(kubectl completion bash)", ". <(echo 'export A=1')",
    "python3 < <(echo 'print(1)')", "sudo bash < <(echo 'ls -la')", "echo ls | sudo sh -c 'cat | sh'",
    "bash script.sh < input.txt", "python3 tool.py < data.txt", "bash -x build.sh 2>&1 | tee log",
    "cat notes | grep -c remove", "source ./env.sh && git commit -m 'remove x'",
    "sh -c 'for a; do echo \"$a\"; done' _ x y", "bash -c 'for a in x y; do echo $a; done' _ rm",
    "perl -e 'print shift' hello", "python3 -c 'import sys; print(sys.orig_argv)' x",
    "ipython --c 'print(1)'", "git read-tree -u -m HEAD", "git read-tree --reset HEAD",
    "git submodule deinit sub", "git checkout-index -a", "sudo " * 40 + "git read-tree HEAD",
    "echo 'git submodule deinit sub' | sh",
    # Round 20 (qanorm19, gemnorm19): forms of the new rules that remove nothing
    "sh -c '\"$@\"' _ fd -e py", "sudo sh -c '\"$@\"' _ fd -x wc -l",
    "echo whoami | sudo -s", "echo ls | su -", "sudo -i", "su - bob", "echo 'rm x' | su -c ls bob",
    "echo 'rm x' | sudo -s ls",
    "sh -c 'echo \"$1\"' _ hello", "sh -c '$1' _ 'ls -la'",
    "python3 -c 'import sys; print(sys.argv[1])' 'hello world'", "perl -e 'print shift' 'a b'",
    "echo 'echo hi' > c.sh && bash c.sh", "bash c.sh > out.log", "echo rm x > notes.txt",
    "bash c.sh > /dev/null; echo rm", "./build.sh > build.log; echo remove",
    "chroot /srv sh -c 'ls'", "watch -n 2 sh -c 'date'", "echo ls | chroot /srv sh", "ssh host uptime",
    "ssh host 'ls /srv'", "echo ls | ssh host", "echo 'rm x' | ssh -n host uptime",
    "awk 'BEGIN{system(\"date\")}'", "awk '/remove/ {n++} END {print n}' log", "awk -F'|' '{print $2}' f",
    "sed -n '/rm/p' f", "sed 's/remove/delete/' f", "sed --sandbox 's/x/rm/e' f",
    "ipython --InteractiveShellApp.code_to_run='print(1)'",
    "ipython --InteractiveShellApp.exec_lines='[\"import numpy as np\"]'",
    # (round 39, qanorm38 F1: git checkout --theirs x and git checkout --ours x overwrite a conflict
    # resolution and moved to the deny rows; these two rows keep their row ids)
    "git restore --staged x", "git switch -m main",
    # Round 21 (qanorm20 F1-F3): forms that remove nothing
    "timeout --kill=1 5 make test", "sudo --us root ls /root", "env --un X printenv", "nice --adj 5 cargo build",
    "timeout --pre 5 git status", "env --un X git clean -n", "taskset --pi 1234", "chrt --ma",
    "awk -v n=5 'BEGIN{system(\"date\")}'", "awk -v pat=remove '$0 ~ pat {n++} END {print n}' log",
    "awk '{print | \"sort\"}' data.txt", "C=1 awk 'BEGIN{system(\"date\")}'",
    "awk 'BEGIN{print ARGV[1]}' 'rm x'", "env C=1 awk 'BEGIN{system(ENVIRON[\"C\"])}'",
    "git lgo -1 --oneline", "git co main", "git st", "git -c color.ui=auto status",
    "git -c help.format=html help log", "git lfs pull", "git config user.name x", "sudo git lfs pull",
    # Round 22 (qanorm21 N1): a command it cannot parse with no removal word or round 15 removal form
    "coproc NAME { echo hi; }; git status", "coproc NAME { echo hi; }\ncargo build",
    "x=$(case a in a) echo hi;; esac); git status", "x=$(case a in a) echo hi;; esac)\ngit reset --soft HEAD~1",
    "shopt -s extglob; echo !(x); ls", "shopt -s extglob; echo !(x)\ngit stash list",
    # Round 23 (qanorm22 F1-F3): an unknown command word before an ordinary cargo or rsync call, rsync
    # options that are not deleting, and python names bound to something other than an os module
    "mywrap cargo build", "chroot /srv cargo test", "time-it cargo build --release", "watch -n 5 cargo check",
    "mywrap cargo clean -h", "mywrap rsync -a src/ dst/", "chroot /srv rsync -av --dry-run a/ b/",
    "mywrap rsync -a --delay-updates a/ b/", "rsync -a --dela a/ b/", "rsync -a --remote-option=-v a b",
    "python3 -c \"import os; o = os.path; print(o.join('a', 'b'))\"",
    "python3 -c \"import os; o = os; print(o.getcwd())\"",
    "python3 -c \"items = [1, 2]; items.remove(1); print(items)\"",
    # Round 24 (qanorm23 F1): a walrus, a conditional expression and a literal-indexed tuple or list
    # element in an ordinary python -c program that removes nothing
    "python3 -c \"import os; print((p := os.getcwd()))\"",
    "python3 -c \"import os; print((o := os).path.join('a', 'b'))\"",
    "python3 -c \"import os; print((os if 1 else None).getcwd())\"",
    "python3 -c \"import os; o = os if True else None; print(o.name)\"",
    "python3 -c \"import os; print((os,)[0].sep)\"",
    "python3 -c \"import os; print([0, os][-1].getpid())\"",
    "python3 -c \"import os; ([1], os)[0].remove(1)\"",
    "python3 -c \"xs = [1, 2]; (xs if xs else []).remove(1); print(xs)\"",
    "python3 -c \"xs = [[1, 2]]; xs[0].remove(1); print(xs)\"",
    "python3 -c \"import shutil; print((s := shutil).which('git'))\"",
    "python3 -c \"import shutil; print((shutil if 1 else None).disk_usage('.'))\"",
    "python3 -c \"import pathlib; print((pathlib,)[0].Path('.').resolve())\"",
    # Round 25 (qanorm24 MEDIUM 1), round 26 (qanorm25 F1) and round 27 (qanorm26 F1 to F3): ordinary
    # xargs use with a shell, su, flock, python, ipython, perl, awk, sed or another program that can run
    # code; round 46 moved those rows to _CANNOT_PARSE_CASES (_appended_command_check). This one remains:
    "echo xargs sh | grep -c 'rm'",
    # Round 28 (qanorm27 N1, N2): ordinary xargs -a use with no written file, and ordinary GNU parallel,
    # sem, xe and rush use
    "xargs -a list.txt wc -l",
    "ls > list.txt; xargs -a list.txt wc -l",
    "ls *.txt | parallel wc -l",
    "parallel --pipe wc -l < big.txt",
    "ls | xe wc -l",
    "echo parallel sh | grep -c 'rm'",
    # Round 29 (qanorm28): writes to the character devices, and ordinary parallel and xe use next to a
    # removal word that is only data
    "make 2>/dev/stderr; bash build.sh; echo rm", "bash build.sh > /dev/tty; echo remove",
    "bash build.sh | tee /dev/stdout; echo rm", "dd if=/dev/zero of=/dev/null count=1; bash b.sh; echo rm",
    "ls *.rm | parallel --tag wc -l {}", "printf 'rm-list.txt' | parallel -k wc -l",
    "ls *.rm | parallel -I@ wc -l @", "cat rm-notes.txt | xe -N1 wc -l", "parallel echo ::: rm-old",
    "cp a.txt b.txt; git commit -m 'remove x'",
    "echo hi > out.txt; sh -c 'make all'; echo rm", "python3 -c 'print(1)'; bash build.sh; echo rm",
    # Round 25 (qanorm24 MINOR 1 and MINOR 2): or, and and methodcaller in an ordinary python -c program
    "python3 -c \"import os; print((os or None).getcwd())\"",
    "python3 -c \"import os; print(os.environ.get('HOME') or '/')\"",
    "python3 -c \"xs = [1, 2]; (xs or []).remove(1); print(xs)\"",
    "python3 -c \"import os; ([1] and [2, 1]).remove(1)\"",
    "python3 -c \"import operator; xs = [1, 2]; operator.methodcaller('remove', 1)(xs); print(xs)\"",
    "python3 -c \"import operator; print(operator.methodcaller('upper')('a'))\"",
    "python3 -c \"import operator, os; print(operator.methodcaller('getcwd')(os))\"",
    # Round 30 (qanorm29 F1): ordinary git submodule update with no -f or --force
    "git submodule update", "git submodule update --init --recursive", "git submodule update --checkout",
    "git submodule update --remote --merge", "git submodule update --rebase sub", "git submodule update -N",
    "git submodule update --init -- \"$path\"", "git submodule update --init --depth 1 --jobs 4",
    "git submodule update --init --filter=blob:none", "sudo git submodule update --init",
    "python3 -c 'import os; os.system(\"git submodule update --init\")'",
    # Round 31 (qanorm30 MINOR-1): ordinary git rebase and git am with no --abort or --skip
    "git rebase --continue", "git rebase --quit", "git rebase --autosquash -i main", "git rebase --edit-todo",
    "git rebase --onto main topic~3 topic", "git am 0001-fix.patch", "git am --continue",
    "git am -3 --signoff 0001-fix.patch", "git am --show-current-patch",
    "python3 -c 'import os; os.system(\"git rebase --continue\")'",
    # Round 37 (grc round 36 MEDIUM): the five commands a session runs on this file, under its name with
    # underscores (the earlier name no-remove-guard.py holds remove at a hyphen boundary)
    "python3 -I draft-offpath/norm1/no_remove_guard.py --self-test",
    "sha256sum draft-offpath/norm1/no_remove_guard.py",
    "git add draft-offpath/norm1/no_remove_guard.py",
    "git diff draft-offpath/norm1/no_remove_guard.py",
    "git commit -m 'no_remove_guard: round 37' draft-offpath/norm1/no_remove_guard.py",
    # Round 37 (grc round 36 LOW): git merge and git cherry-pick without --abort, and the mv forms (round 38: only
    # --backup=numbered is advised; mv -n stays allowed)
    "git merge --continue", "git merge --quit", "git merge main", "git cherry-pick --continue",
    "git cherry-pick --quit", "git cherry-pick abc123",
    "mv --backup=numbered x /tmp/grc/deleteme/", "mv -n x /tmp/deleteme-grc/",
    # Round 38 (qanorm37 F1): the actions of git's lists that reset nothing stay allowed (--quit, --continue
    # and the like), and so does an ordinary revert, cherry-pick or am
    "git revert --continue", "git revert --quit", "git revert abc123", "git revert --no-edit abc123",
    "git am --quit", "git am --resolved", "git cherry-pick --signoff abc123",
    "git revert --strategy=ours abc123",
    # Round 39 (qanorm38 F1): git checkout and git restore with no stage-rewrite option, or with none that
    # names a path, and option values that only look like one
    "git restore x", "git restore -W x", "git restore -p x", "git restore --ignore-unmerged x",
    "git restore --overlay x", "git restore -sm x", "git restore -U3 -p x", "git checkout -m",
    "git checkout -bm", "git checkout -b m main", "git checkout --orphan m", "git switch --merge main",
    "git switch --conflict=diff3 main",
    # Round 40 (qanorm39 F1 to F4): an abbreviated value option, -U with an attached value, xargs with no
    # stage-rewrite option, a pathspec file with none, and an operation ref that names no path
    "git checkout --conf merge", "git checkout -U3 -p main -- f",
    "git checkout --pathspec-fr=list",
    "git checkout -b x MERGE_HEAD",
    # Round 41 (qanorm40 N1, N4, N7, N8): the appended-path check finds nothing in a routine git command,
    # ORIG_HEAD stays allowed, and --end-of-options alone denies nothing
    "find . -execdir git log -1 -- {} ';'",
    "git checkout ORIG_HEAD -- f",
    "git restore --end-of-options f", "git checkout --end-of-options main",
    # Round 42 (qanorm41 F1 to F3, F5): the table reads routine commands, a name that only starts like an
    # operation ref is not one, find -exec without {} appends nothing, and gfind and bfs list as find does
    "ls | parallel --tty git log -1", "git checkout main auto_merge.py",
    "git checkout main fetch_head.txt", "git checkout HEAD Merge_Head.md", "git checkout -p main auto_merge.c",
    "git checkout auto_merge-fix -- f", "git restore -s auto_merge-fix f",
    "find . -name x -exec git checkout -m ';'", "find . -name '*.c' -exec git restore --theirs ';'",
    "find . -name '*.c' -execdir git checkout -m ';'", "find . -ok git checkout MERGE_HEAD ';'",
    "gfind . -name x -print", "bfs . -name x",
    # Round 43 (qanorm42 N1 to N3): the git rule behind a path-adding program reads only the subcommand
    # (a git value option's value and an expansion in another command are not one), and the right side
    # of A...B is not matched
    "ls | xargs -I{} mv {} \"$a\" \"$b\"", "ls | parallel -S host git log -1",
    "git checkout HEAD...main -- f",
    # Round 45 (qanorm44 F1, F2): behind a path-adding program, git with a listed subcommand
    # (_GIT_APPENDED_ALLOWED) as the word right after git passes
    "git diff --name-only | xargs git log --oneline --", "git ls-files | xargs git blame --line-porcelain",
    "fd -e c -X git status --short", "fd -e py -x git log -1 --format=%H --",
    "find . -name '*.c' -exec git diff --stat {} +", "ls | parallel git show HEAD:{}", "ls | sem git ls-files",
    "ls | xe git rev-parse --verify", "ls | rush git cat-file -t", "git ls-files | gxargs git ls-tree HEAD",
    "ls | xargs -0 git check-ignore", "ls | xargs git shortlog -s --",
    "ls | xargs git rev-list -n1 HEAD --", "ls | parallel -j4 git diff --stat",
    "fdfind -e md -X git log --oneline", "ls | xargs -0 -r -n1 git log -1 --",
    # Round 46 (qanorm45): probes that stay allowed: a listed plain program behind a path-adding
    # program, and the residual forms the review names (F3 --output of a listed git subcommand, a
    # shell redirect, F5 a GIT_ setting at top level; see RESIDUAL)
    'ls | xargs git rev-list --output=src.c HEAD',
    'ls | xargs git blame --output=src.c',
    'ls | xargs git log --output=.git/HEAD',
    "printf -- '--output=.git/HEAD\\n' | xargs git log",
    'echo x > .git/HEAD',
    ': > src.c',
    'git log > .git/index',
    'GIT_EXTERNAL_DIFF=./fix.sh git diff',
    'GIT_PAGER=./fix.sh git log',
    'ls | xargs ls -lS',
    "ls | xargs grep -l 'gi[t]'",
    'ls | xargs grep -l x',
    'ls | parallel grep -l x',
    'fd -e c -X grep -l x',
    "find . -name '*.c' -exec grep -l x {} +",
    'ls | xargs',
    # Round 47 (qanorm46): the forms the round 46 review found allowed, pinned at their current verdict
    # (allowed; no logic changes in round 47): B1 xe -p, B2 an exported bash function, M1 a setting name
    # built at run time, M2 --parens, M3 an alias in the same command, m1 --limit and file-writing
    # options (see RESIDUAL, the round 47 item)
    "ls | xe -p cat cat + '*' env -S'git restore --ours'",
    "ls | env 'BASH_FUNC_grep%%=() { git restore --ours \"$@\"; }' parallel grep x",
    "export 'BASH_FUNC_grep%%=() { git restore --ours \"$@\"; }'; ls | parallel grep x",
    "env 'BASH_FUNC_x%%=() { git restore --ours f; }' bash -c x",
    'v=PARALL; export "${v}EL=-I log"; echo restore | parallel git log --ours f',
    'v=GI; export "${v}T_EXTERNAL_DIFF=./fix.sh"; ls | xargs git diff',
    'export $(cat env.txt); ls | xargs git diff',
    "ls | parallel --parens ,,,, grep x ',,system \"gi\".\"t restore --ours f\",,'",
    "ls | parallel --PARE ,,,, grep x ',,system \"gi\".\"t restore --ours f\",,'",
    "ls | sem --parens ,,,, grep x ',,system \"gi\".\"t restore --ours f\",,'",
    "shopt -s expand_aliases\nalias xargs='env -S\"git restore --ours\"'\nls | xargs grep x",
    "shopt -s expand_aliases\nalias ll='git restore --ours'\nll f",
    "ls | parallel '--limit=./x.sh' cat",
    'ls | parallel --joblog src.c cat',
    'ls | parallel --results src.c cat',
    'ls | parallel --tmpl a.tmpl=src.c cat',
    'ls | rush -o src.c cat',
    # Round 48 (grc review of round 47): the forms that review found allowed and RESIDUAL did not name,
    # pinned at their current verdict (allowed by both layers; no logic changes in round 48): MED-2 git
    # apply, git am and patch with a diff that deletes a file (also -R, -E and a here-document), MED-3 git
    # sparse-checkout set, LOW-1 git stash drop, git stash clear and git gc --prune=now, LOW-2 pip, npm and
    # cargo uninstall (see RESIDUAL, the round 48 item)
    "git apply fix.patch",
    "git apply -R fix.patch",
    "git am 0001-drop-old.patch",
    "patch -p1 < fix.patch",
    "patch -R -p1 < fix.patch",
    "patch -E -p1 < fix.patch",
    "git apply <<'EOF'\ndiff --git a/old.c b/old.c\ndeleted file mode 100644\nindex 0000001..0000000\n"
    "--- a/old.c\n+++ /dev/null\n@@ -1 +0,0 @@\n-int x;\nEOF",
    "git am <<'EOF'\nFrom: a <a@example.com>\nSubject: [PATCH] drop old.c\n\n---\n"
    "diff --git a/old.c b/old.c\ndeleted file mode 100644\nindex 0000001..0000000\n"
    "--- a/old.c\n+++ /dev/null\n@@ -1 +0,0 @@\n-int x;\nEOF",
    "patch -p1 <<'EOF'\n--- a/old.c\n+++ /dev/null\n@@ -1 +0,0 @@\n-int x;\nEOF",
    "patch -E -p1 <<'EOF'\n--- a/old.c\n+++ /dev/null\n@@ -1 +0,0 @@\n-int x;\nEOF",
    "git sparse-checkout set src",
    "git stash drop",
    "git stash clear",
    "git gc --prune=now",
    "pip uninstall -y requests",
    "npm uninstall left-pad",
    "cargo uninstall ripgrep",
    # Round 48 (grc review of round 47): sha256sum of the path of the file actually running, so an
    # installer copy or rename whose path the broad layer refuses fails this row (an allow row passes only
    # when the inner layer allows it, and a broad-layer refusal of a row not pinned by id below fails the
    # pin check, so this row expects allow from both layers). Round 49 (grc review of round 48): the path
    # is os.path.abspath(__file__), the installed name as the self-test was started with it, not
    # os.path.realpath(__file__), which resolved a symlink installed under a refused name to its allowed
    # target, so the row passed there; abspath resolves no symlink, so this row tests the name itself.
    # Round 51 (grc review of round 50): since Python 3.9 the main script's __file__ is already absolute
    # (witnessed with python3 3.14.4 for a relative start, a relative start through a symlink and an
    # importlib load from a relative path), so abspath is kept for what still holds: unlike realpath it
    # resolves no symlink, so a symlinked install is tested by its own name; it is a no-op guard for a
    # loader or a Python before 3.9 that leaves __file__ relative (not witnessed). The broad row on
    # no-remove-guard.py in _BROAD_CASES shows only that the broad layer refuses the same command on a
    # refused name in this directory; that this row would then fail its pin check is inference.
    "sha256sum " + shlex.quote(os.path.abspath(__file__)),
    # Round 50 (grc review of round 49): GNU patch reads --rem (also --remo, --remov) as an unambiguous
    # prefix of --remove-empty-files, the long spelling of -E; none holds the word remove, so both layers
    # allow them (see RESIDUAL, the round 48 item, MED-2)
    "patch --rem -p1 < fix.patch",
    "patch --rem -p1 <<'EOF'\n--- a/old.c\n+++ /dev/null\n@@ -1 +0,0 @@\n-int x;\nEOF",
    # Round 51 (grc review of round 50): the --remo and --remov file forms, so each abbreviation the
    # RESIDUAL round 48 item names has an allow row
    "patch --remo -p1 < fix.patch",
    "patch --remov -p1 < fix.patch",
)

# Round 32 (D-2385): the _ALLOW_CASES rows the broad layer refuses (each row still passes the inner layer).
# Round 34 (qanorm33 N5): pinned by row id (the index in _ALLOW_CASES), not by a count, so a change that
# swaps which rows are refused fails too; round 34 adds row 296 (source ./env.sh && git commit -m ...,
# whose sourced script may run the message: see BROAD LAYER). Round 35 (qanorm34 N2) adds rows 20, 295,
# 440, 459 and 470 (a pipeline into grep, or a second command before git commit: see BROAD LAYER).
# Round 45 moves 16 rows (ids 425 to 427 and 537 to 569 of round 44) to _CANNOT_PARSE_CASES, none of them
# pinned here, so the pinned ids above 427 move down by 3 (round 35's 440, 459 and 470 are 437, 456 and
# 467); the same 155 commands are pinned.
# Round 46 (qanorm45 F1, F2, F4) moves 58 rows (round 45 ids 266, 395 to 436, 439 to 441, 443, 444, 446
# to 449, 451, 452, 454, 455, 466 and 566) to _CANNOT_PARSE_CASES; one of them was pinned here (441, xargs
# -a cmds.txt sh -c; echo rm, which the inner layer now refuses), so 154 commands stay pinned, at ids that
# move down by the number of moved rows before each; none of the 16 rows round 46 adds is refused.
# Round 47 appends 17 rows (qanorm46's allowed forms) after the last row, so no id moves; none of them
# is refused. Round 48 appends 18 rows (17 forms of the grc review of round 47 and the real-path
# sha256sum row) after the last row, so no id moves; none of them is refused. Round 49 changes the
# sha256sum row in place (abspath for realpath), so no id moves; it is still not refused. Round 50 appends
# 2 rows (patch --rem with a diff file and with a here-document) after the last row, so no id moves; none
# of them is refused. Round 51 appends 2 rows (patch --remo and patch --remov with a diff file) after the
# last row, so no id moves; none of them is refused.
_BROAD_REFUSED_ALLOW_ROWS = frozenset((
    0, 1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 16, 17, 20, 21, 22, 23, 24, 25, 28, 29, 36, 37, 39, 40, 41, 42, 43,
    44, 45, 49, 50, 51, 52, 54, 55, 56, 57, 58, 61, 62, 63, 64, 70, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
    91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 113, 114, 117, 119, 121, 122, 125,
    127, 128, 130, 134, 137, 141, 142, 143, 146, 155, 157, 158, 161, 162, 163, 164, 166, 167, 168, 169, 172,
    174, 192, 193, 201, 202, 203, 204, 205, 206, 211, 212, 219, 224, 229, 238, 248, 260, 274, 294, 295, 297,
    313, 314, 321, 322, 323, 330, 332, 334, 335, 336, 346, 350, 353, 373, 381, 388, 389, 390, 394, 400, 401,
    402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 415, 416, 417))

# Round 32 (D-2385, D-2384): commands the inner layer allows and the broad layer refuses
_BROAD_CASES = (
    # moved from _CANNOT_PARSE_CASES: the removal word is outside any here-document body, or the body
    # has it outside command position, and no exception applies
    "cat <<EOF\nhello\nEOF\ngit rm x",
    "cat 3<<EOF\nhello\nEOF\necho delete",
    # (round 34, qanorm33 N3: the python3 -c "$(cat <<'PY' ...)" row moved to _RULE_CASES, cannot-parse)
    "cat <<'EOF' > notes.md\nremove the stale cache\nEOF",
    # ordinary commands with a removal word or form outside the exceptions
    "echo rm -rf x", "git status; make clean", "kubectl delete pod x",
    # shapes next to the exceptions that the exceptions do not cover
    "gh pr create --title 'remove the cache' --body x", "gh repo create x --description 'remove x'",
    "sudo git commit -m 'remove x'", "git commit -m fix rm-notes.txt", "git commit -m \"$(echo remove)\"",
    "git commit -m \"$(cat <<'EOF'\nremove x\nEOF\n)$(echo)\"",
    "git commit -F - <<EOF\nremove $HOME\nEOF", "git commit -F notes.txt <<'EOF'\nremove x\nEOF",
    "git commit -F - <<'EOF'\nremove x\nEOF\necho rm",
    "ls | xargs grep -l remove", "grep -f rm-patterns.txt src", "grep --frobnicate 'remove' f",
    "rg --pre 'rm -rf x' foo .", "grep -e x 'remove' f",
    # round 33 rule rows that round 34 refuses by two rules (exact command word and PATH binding)
    "PATH=.:/usr/bin git commit -F - <<'EOF'\nmywrap rm -rf x\nEOF",
    "PATH=.:/usr/bin; gh pr create --body 'rm -rf x'",
    # Round 34 (qanorm33 N1, N2): routes that more than one round 34 rule refuses
    "git config core.editor sh && git commit -e -m 'rm -rf x'",
    "export GIT_EDITOR=sh\ngit commit -e -m 'rm -rf x'",
    "git commit --allow-empty -m 'rm -rf x'; sh .git/COMMIT_EDITMSG",
    "git commit --allow-empty -m 'rm -rf x'; source .git/COMMIT_EDITMSG",
    "git commit --allow-empty -F - <<'EOF'\nR=rm; $R -rf x\nEOF\nsh .git/COMMIT_EDITMSG",
    "git commit -m 'rm -rf x' && git -c alias.y='!sh .git/COMMIT_EDITMSG' y",
    # Round 49 (grc review of round 48): patch --remove-empty-files, the long spelling of patch -E, holds
    # the removal word remove, so the broad layer refuses it (the -E rows are allow rows; see RESIDUAL,
    # the round 48 item, MED-2)
    "patch --remove-empty-files -p1 < fix.patch",
    "patch --remove-empty-files -p1 <<'EOF'\n--- a/old.c\n+++ /dev/null\n@@ -1 +0,0 @@\n-int x;\nEOF",
    # Round 50 (grc review of round 49): a patch here-document whose diff holds a line with a removal word
    # (rm x;) is refused by the broad layer, an over-refusal in the safe direction (see BROAD LAYER)
    "patch -p1 <<'EOF'\n--- a/build.sh\n+++ b/build.sh\n@@ -1 +1 @@\n-rm x;\n+echo x;\nEOF",
    # Round 50 (grc review of round 49), reworded at round 51 (grc review of round 50): the command of the
    # own-path row of _ALLOW_CASES built on a refused name, the earlier name no-remove-guard.py, in the
    # directory the own-path row derives (os.path.dirname of os.path.abspath(__file__)). The row shows
    # only that the broad layer refuses this command text; no file of that name is installed or hashed,
    # and that an install under that name would fail the own-path allow row (absent from
    # _BROAD_REFUSED_ALLOW_ROWS, so a broad refusal of it fails the pin check) is inference. The name is
    # fixed on purpose: the own-path allow row already tests the installed name, and this control must be
    # refused on every install, while the name the own-path check derives (the installed name itself) is
    # allowed on the shipped no_remove_guard.py and on any allowed rename, so a control on it could not
    # expect refusal there; only the directory, which the two can share, comes from the install.
    "sha256sum " + shlex.quote(os.path.join(os.path.dirname(os.path.abspath(__file__)), "no-remove-guard.py")),
    # Round 53 (grc field data from the live guard): record, ledger and memory lines that erase nothing
    # but mention a removal word are refused (see BROAD LAYER, the round 53 over-refusal note); synthetic
    # lines in the shapes of grc's four lines: a record line naming the guard with a hyphen or a space
    # (two rows), a ledger line that the session must never use rm, and a memory index line linking a
    # note whose name holds a removal word at a hyphen boundary
    "echo '- 2026-01-01: the no-remove guard refused a status line' >> notes/record.md",
    "cat >> notes/record.md <<'EOF'\n- round 9: no-remove-guard refused one line, reissued without it\nEOF",
    "echo '- rule: this session must never use rm on a tracked file' >> notes/ledger.md",
    "echo '- [Set-aside policy](feedback-delete-policy.md): move, never erase' >> memory/MEMORY.md",
)

# Round 32 (D-2385, D-2384): each row passes with its rule in place and fails with that rule reverted
# (the self-test sets the _RULES entry to False for the row). An exception row holds a removal word only
# in the text the exception covers; a here-document row holds it in a body.
_RULE_CASES = (
    ("git commit message", "git commit -m 'remove the stale cache'", ALLOW),
    ("git commit message", "git commit -am \"delete the unused helper\"", ALLOW),
    ("git commit message", "git commit --message='rm wrapper dropped' --signoff", ALLOW),
    ("git commit message", "git -C repo commit -q -m'remove x'", ALLOW),
    ("git commit message", "git commit -F rm-notes.txt", ALLOW),
    ("git commit message", "git commit --file=rm-notes.txt", ALLOW),
    ("git commit message", "git commit -F - <<'EOF'\nfix: remove the stale cache\nEOF", ALLOW),
    ("gh body", "gh pr create --title 'Cache fix' --body 'remove the stale cache'", ALLOW),
    ("gh body", "gh issue create -t Bug -b 'rm fails on x'", ALLOW),
    ("gh body", "gh pr comment 12 --body-file=rm-notes.md", ALLOW),
    ("gh body", "gh issue comment 7 --body=delete", ALLOW),
    ("gh body", "gh pr create --title x --body-file - <<'EOF'\n- remove the stale cache\nEOF", ALLOW),
    ("grep or rg pattern", "grep -n 'remove' notes.txt", ALLOW),
    ("grep or rg pattern", "grep -rn -e delete -e 'unlink' src", ALLOW),
    ("grep or rg pattern", "grep -A 2 --include='*.py' -- -delete src", ALLOW),
    ("grep or rg pattern", "rg 'rmtree' src", ALLOW),
    ("grep or rg pattern", "rg -n --regexp=getattr -g '*.py' .", ALLOW),
    # (round 35: the cd src && rg ... row moved to the simple command allowlist rows, as a list is refused)
    ("grep or rg pattern", "rg -i -t py 'os[.]remove' src", ALLOW),
    ("here-document command position", "git commit -F - <<'EOF'\nrm -rf x\nEOF", CANNOT_PARSE),
    ("here-document command position", "git commit -m \"$(cat <<'EOF'\nfix\n(rm -rf x)\nEOF\n)\"",
     CANNOT_PARSE),
    ("here-document command position", "gh pr create --body-file - <<'EOF'\nsudo rm -rf x\nEOF", CANNOT_PARSE),
    ("here-document command position", "git commit -F - <<'EOF'\nok; git clean -fdx\nEOF", CANNOT_PARSE),
    ("here-document narrowing", "git commit -m \"$(cat <<'EOF'\nremove the old rm helper\nEOF\n)\"", ALLOW),
    ("here-document narrowing", "git commit -F - <<'EOF'\nfix: delete the stale rm wrapper\nEOF", ALLOW),
    ("here-document narrowing",
     "gh pr create --title x --body \"$(cat <<'EOF'\n## Summary\n- remove the cache\nEOF\n)\"", ALLOW),
    ("here-document narrowing", "git commit -m \"$(cat <<-EOF\n\tdrop the rmdir call\n\tEOF\n)\"", ALLOW),
    # Round 33 (qanorm32 F1): a body line that starts with the delimiter; bash ends the here-document and
    # the substitution there and runs the next line
    ("here-document delimiter prefix", "git commit -m \"$(cat <<'EOF'\nmsg\nEOF)\"\nmywrap rm -rf x\nEOF\n)\"",
     BROAD),
    ("here-document delimiter prefix", "git commit -m \"$(cat <<EOF\nmsg\nEOF)\"\nmywrap rm -rf x\nEOF\n)\"",
     BROAD),
    ("here-document delimiter prefix",
     "gh pr create --title t --body \"$(cat <<'EOF'\nmsg\nEOF)\"\nmywrap rm -rf x\nEOF\n)\"", BROAD),
    # Round 33 (qanorm32 F1, F2): a removal behind a redirection, coproc or time -p in a here-document body
    ("here-document command words",
     "git commit -m \"$(cat <<'EOF'\nmsg\nEOF)\"\n2>/dev/null rm -rf x\nEOF\n)\"", CANNOT_PARSE),
    ("here-document command words", "git commit -F - <<'EOF'\n2>/dev/null rm -rf x\nEOF", CANNOT_PARSE),
    ("here-document command words", "git commit -F - <<'EOF'\n2>&1 rm -rf x\nEOF", CANNOT_PARSE),
    ("here-document command words", "git commit -F - <<'EOF'\ncoproc rm -rf x\nEOF", CANNOT_PARSE),
    ("here-document command words", "git commit -F - <<'EOF'\ntime -p rm -rf x\nEOF", CANNOT_PARSE),
    ("here-document command words",
     "gh pr create --title x --body-file - <<'EOF'\n&>/dev/null find . -delete\nEOF", CANNOT_PARSE),
    ("here-document command words", "git commit -F - <<'EOF'\n{ >/dev/null git clean -fdx; }\nEOF",
     CANNOT_PARSE),
    # Round 33 (qanorm32 F3): a command word that is not exactly git, gh, grep or rg, a NAME=VALUE word
    # before it, or the word PATH elsewhere in the command
    # (round 34: the two PATH rows moved to _BROAD_CASES, as the PATH binding rule refuses them too)
    ("exact command word", "./git commit -F - <<'EOF'\nmywrap rm -rf x\nEOF", BROAD),
    ("exact command word", "/tmp/x/git commit -m 'rm -rf x'", BROAD),
    ("exact command word", "./grep -e 'rm -rf x' f", BROAD),
    ("exact command word", "X=1 rg 'rm -rf x'", BROAD),
    # Round 33 (qanorm32 F4): a function defined in the command with the name of the exempt command word
    # (round 34: the four sh -c "$N" rows moved to _CANNOT_PARSE_CASES, as the interpreter program
    # expansion rule denies them; these bodies run the message through a wrapper the guard does not know)
    ("function shadowing", "git() { mywrap \"$3\"; }; git commit -m 'rm -rf x'", BROAD),
    ("function shadowing", "function gh { mywrap \"$4\"; }; gh pr create --body 'rm -rf x'", BROAD),
    ("function shadowing", "grep () { mywrap \"$2\"; }; grep -e 'rm -rf x' f", BROAD),
    ("function shadowing", "rg() { mywrap \"$1\"; }; rg 'rm -rf x'", BROAD),
    # Round 34 (qanorm33 N1): PATH bound by any builtin form, read after quote and backslash removal, or a
    # binding whose name an expansion supplies
    ("PATH binding", "export PA\"TH\"=.:/usr/bin; git commit -m 'rm -rf x'", BROAD),
    ("PATH binding", "export PA\\TH=.; git commit -m 'rm -rf x'", BROAD),
    ("PATH binding", "export 'PA''TH=.'; git commit -m 'rm -rf x'", BROAD),
    ("PATH binding", "declare -x PA''TH=.; gh pr create --body 'rm -rf x'", BROAD),
    ("PATH binding", "typeset -x PA\"TH\"=.; grep -e 'rm -rf x' f", BROAD),
    ("PATH binding", "printf -v PA\"TH\" %s .; git commit -m 'rm -rf x'", BROAD),
    ("PATH binding", "read -r PA\"TH\" < p.txt; git commit -m 'rm -rf x'", BROAD),
    ("PATH binding", "declare -n p=PA\"TH\"; p=.; git commit -m 'rm -rf x'", BROAD),
    ("PATH binding", "for PA\"TH\" in .; do git commit -m 'rm -rf x'; done", BROAD),
    ("PATH binding", "n=PA; export \"${n}TH\"=.; git commit -m 'rm -rf x'", BROAD),
    # Round 34 (qanorm33 N2): git or gh that start the editor on the message or set configuration that runs
    # a program, and a path to the message file
    ("git editor and configuration", "git -c core.editor=sh commit -e -m 'rm -rf x'", BROAD),
    ("git editor and configuration", "export GIT_EDITOR=sh; git commit -e -m 'rm -rf x'", BROAD),
    ("git editor and configuration", "git config core.editor ./ed.sh && git commit --edit -m 'rm -rf x'",
     BROAD),
    ("git editor and configuration", "git -c core.hooksPath=/tmp/h commit -m 'rm -rf x'", BROAD),
    ("git editor and configuration", "git commit -c HEAD -m 'rm -rf x'", BROAD),
    ("git editor and configuration", "gh pr create -e --body 'rm -rf x'", BROAD),
    ("git editor and configuration", "git commit --allow-empty -m 'rm -rf x'; cp .git/COMMIT_EDITMSG r.sh", BROAD),
    # Round 34 (qanorm33 N2): a command that may run the exempt text the same command stored
    ("exempt text runner", "git commit --allow-empty -m 'rm -rf x'; sh .git/COMMIT_E*", BROAD),
    ("exempt text runner", "git commit --allow-empty -m 'rm -rf x'; . .git/COMMIT_E*", BROAD),
    ("exempt text runner", "git commit --allow-empty -m 'rm -rf x'; chroot / sh .git/C*", BROAD),
    ("exempt text runner", "git commit --allow-empty -m 'rm -rf x'; awk '{system($0)}' .git/C*", BROAD),
    # Round 34 (qanorm33 N3): an interpreter program that a command substitution supplies
    ("interpreter program expansion", "python3 -c \"$(cat <<'PY'\nimport os\nos.remove('x')\nPY\n)\"",
     CANNOT_PARSE),
    ("interpreter program expansion", "python3 -c \"$(cat <<'PY'\nimport shutil\nshutil.rmtree('x')\nPY\n)\"",
     CANNOT_PARSE),
    ("interpreter program expansion", "x=$(cat <<'PY'\nimport os\nos.remove('x')\nPY\n); python3 -c \"$x\"",
     CANNOT_PARSE),
    ("interpreter program expansion", "git commit -m 'rm -rf x' && sh -c \"$(git log -1 --format=%B)\"",
     CANNOT_PARSE),
    # Round 34 (qanorm33 N4): a reader behind uv run, pipx run, poetry run, jobs -x or flock
    ("runner readers", "uv run sh < <(echo 'rm -rf x')", CANNOT_PARSE),
    ("runner readers", "pipx run sh < <(echo 'rm -rf x')", CANNOT_PARSE),
    ("runner readers", "poetry run . <(echo 'rm -rf x')", CANNOT_PARSE),
    ("runner readers", "jobs -x sh < <(echo 'rm -rf x')", CANNOT_PARSE),
    ("runner readers", "uv run bash /dev/fd/3 3< <(echo 'rm -rf x')", CANNOT_PARSE),
    ("runner readers", "flock /tmp/l . <(echo 'rm -rf x')", CANNOT_PARSE),
    # Round 35 (qanorm34 N2): the exceptions apply only to one simple command of an allowlisted form
    # B1: git's command runners fed the exempt text through a substitution or a variable
    ("simple command allowlist", "git commit -m 'rm -rf x' && git rebase -x \"$(git log -1 --format=%B)\" HEAD~1",
     BROAD),
    ("simple command allowlist",
     "git commit -m 'rm -rf x' && git rebase --exec=\"$(git log -1 --format=%B)\" HEAD~1", BROAD),
    ("simple command allowlist", "git commit -m 'rm -rf x'; m=$(git log -1 --format=%B); git rebase -x \"$m\" HEAD~1",
     BROAD),
    ("simple command allowlist",
     "git commit -m 'git reset --hard' && git submodule foreach \"$(git log -1 --format=%B)\"", BROAD),
    ("simple command allowlist", "git commit -m 'rm -rf x' && git bisect run \"$(git log -1 --format=%B)\"", BROAD),
    ("simple command allowlist",
     "gh pr create -t t -b 'rm -rf x' && git rebase -x \"$(gh pr view --json body -q .body)\" HEAD~1", BROAD),
    ("simple command allowlist",
     "git commit -F - <<'EOF' && git bisect run \"$(git log -1 --format=%B)\"\nremove the cache\nEOF", BROAD),
    # J1: a hook or hooksPath written in the same command under a spelling the round 34 regex misses
    ("simple command allowlist", "printf '#!/bin/sh\\n. \"$1\"\\n' > .git//hooks/commit-msg; "
     "chmod +x .git//hooks/commit-msg; git commit -m 'rm -rf x'", BROAD),
    ("simple command allowlist", "printf '#!/bin/sh\\n. \"$1\"\\n' > .git/./hooks/commit-msg; "
     "chmod +x .git/./hooks/commit-msg; git commit -m 'rm -rf x'", BROAD),
    ("simple command allowlist", "printf '[core]\\n\\thooks\\x50ath = h\\n' >> ~/.gitconfig; git commit -m 'rm -rf x'",
     BROAD),
    # J2: rg --pre runs a program on a file the same command filled with exempt text
    ("simple command allowlist",
     "git commit --allow-empty -m 'rm -rf x' && git log -1 --format=%B > f && rg --pre sh x f", BROAD),
    ("simple command allowlist", "grep -e 'rm -rf x' README > f; rg --pre sh y f", BROAD),
    ("simple command allowlist", "rg --pre=sh 'rm -rf x' f", BROAD),
    # D1: a wrapper the guard does not name fed the message through a substitution
    ("simple command allowlist", "git commit -m 'rm -rf x' && watch -n 1 \"$(git log -1 --format=%B)\"", BROAD),
    ("simple command allowlist", "git commit -m 'rm -rf x' && timeout 5 watch \"$(git log -1 --format=%B)\"",
     BROAD),
    ("simple command allowlist", "git commit -m 'rm -rf x' && chroot / \"$(git log -1 --format=%B)\"", BROAD),
    ("simple command allowlist", "git commit -m 'rm -rf x' && script -qc \"$(git log -1 --format=%B)\" /dev/null",
     BROAD),
    # moved from the grep or rg pattern rows: a list is not one simple command
    ("simple command allowlist", "cd src && rg -i -t py 'os[.]remove'", BROAD),
)
# Round 35 (qanorm34 N2): the simple command allowlist also refuses every row of these round 33 and round
# 34 rules, so the self-test reverts it together with the row's own rule, to show that each rule still
# refuses its rows on its own
_ALLOWLIST_SUBSUMED_RULES = frozenset(("exact command word", "function shadowing", "PATH binding",
                                       "git editor and configuration", "exempt text runner"))

# Round 36 (qanorm35 R2): one row per short option of _RG_ALLOW and its long spelling (ripgrep 15.1.0
# rg --help), with the value a value option takes ("" for none). The self-test runs rg OPTION -e 'rmtree'
# src with each spelling, requires allow for both, and requires that the rows name every short letter of
# _RG_ALLOW and only long options of _RG_ALLOW of the same kind, so a short option added without its long
# spelling, or a row whose long spelling _RG_ALLOW leaves out, fails
_RG_SPELLING_PAIRS = (
    ("-A", "--after-context", "2"), ("-B", "--before-context", "2"), ("-C", "--context", "2"),
    ("-d", "--max-depth", "2"), ("-d", "--maxdepth", "2"), ("-E", "--encoding", "utf-8"),
    ("-e", "--regexp", "'unlink'"), ("-f", "--file", "pats.txt"), ("-g", "--glob", "'*.py'"),
    ("-j", "--threads", "1"), ("-M", "--max-columns", "80"), ("-m", "--max-count", "1"),
    ("-r", "--replace", "x"), ("-t", "--type", "py"), ("-T", "--type-not", "js"),
    ("-0", "--null", ""), ("-.", "--hidden", ""), ("-a", "--text", ""), ("-b", "--byte-offset", ""),
    ("-c", "--count", ""), ("-F", "--fixed-strings", ""), ("-H", "--with-filename", ""), ("-h", "--help", ""),
    ("-I", "--no-filename", ""), ("-i", "--ignore-case", ""), ("-L", "--follow", ""),
    ("-l", "--files-with-matches", ""), ("-N", "--no-line-number", ""), ("-n", "--line-number", ""),
    ("-o", "--only-matching", ""), ("-p", "--pretty", ""), ("-P", "--pcre2", ""), ("-q", "--quiet", ""),
    ("-S", "--smart-case", ""), ("-s", "--case-sensitive", ""), ("-U", "--multiline", ""),
    ("-u", "--unrestricted", ""), ("-V", "--version", ""), ("-v", "--invert-match", ""),
    ("-w", "--word-regexp", ""), ("-x", "--line-regexp", ""),
)

_FAIL_CLOSED_CASES = (
    ("payload without tool_name", {"tool_input": {"command": "ls"}}),
    ("Bash payload without tool_input", {"tool_name": "Bash"}),
    ("command that is not a string", {"tool_name": "Bash", "tool_input": {"command": ["rm", "x"]}}),
    ("command holding a NUL", {"tool_name": "Bash", "tool_input": {"command": "ls\x00rm x"}}),
    ("payload that is not JSON", b"not json"),
    ("payload that is not UTF-8", b"\xff\xfe"),
    ("payload that is a JSON array", b"[]"),
    # Round 54 (grc review of rounds 51 to 53): a payload that starts with a UTF-8 byte order mark is
    # malformed input, even when the rest is a Bash payload the guard would allow (see RESIDUAL)
    ("payload that starts with a UTF-8 byte order mark",
     b'\xef\xbb\xbf{"tool_name": "Bash", "tool_input": {"command": "ls"}}'),
)


def _run_case(inp):
    if isinstance(inp, bytes):
        return decide_raw(inp)
    if isinstance(inp, str):
        return decide_payload(_bash(inp))
    return decide_payload(inp)


def _with_deny_logic_off(inp):
    global _DENY_LOGIC_ON
    _DENY_LOGIC_ON = False
    try:
        return _run_case(inp)
    finally:
        _DENY_LOGIC_ON = True


def _self_test():
    results = []  # (group, label, passed, detail)
    flip_checked = 0
    flip_passed = 0

    def record(group, label, passed, detail=""):
        results.append((group, label, passed, detail))

    for group, expected, cases in (("deny", DENY, _DENY_CASES),
                                   ("cannot-parse", CANNOT_PARSE, _CANNOT_PARSE_CASES),
                                   ("broad", BROAD, _BROAD_CASES)):
        for command in cases:
            got = _run_case(command)
            flipped = _with_deny_logic_off(command)
            flip_checked += 1
            flip_ok = flipped == ALLOW
            flip_passed += 1 if flip_ok else 0
            record(group, command, got == expected and flip_ok,
                   "got {}, with the deny logic off got {}".format(got, flipped))
    # Round 32: every allow row still passes the inner layer; the broad layer refuses a counted number
    refused_rows = set()
    for row_id, command in enumerate(_ALLOW_CASES):
        _scan_budget[0] = _SCAN_BUDGET
        inner = _check_command_text(command, 0)
        got = _run_case(command)
        if got == BROAD:
            refused_rows.add(row_id)
        record("allow", command, inner is None and got in (ALLOW, BROAD),
               "inner layer got {}, both layers got {}".format(inner, got))
    broad_refused = len(refused_rows)
    # Round 34 (qanorm33 N5): the refused rows are pinned by id
    record("allow", "broad layer refusals among the allow rows", refused_rows == _BROAD_REFUSED_ALLOW_ROWS,
           "refused but not pinned {}, pinned but not refused {}".format(
               sorted(refused_rows - _BROAD_REFUSED_ALLOW_ROWS), sorted(_BROAD_REFUSED_ALLOW_ROWS - refused_rows)))
    record("allow", "a Write tool call", _run_case({"tool_name": "Write", "tool_input": {}}) == ALLOW)
    # Round 36 (qanorm35 R2): the short and long spelling of each rg option get the same verdict, allow
    for short, long_, value in _RG_SPELLING_PAIRS:
        verdicts = [_run_case("rg {} -e 'rmtree' src".format(" ".join(p for p in (spelling, value) if p)))
                    for spelling in (short, long_)]
        record("allow", "rg spelling pair {} and {}".format(short, long_), verdicts == [ALLOW, ALLOW],
               "{} got {}, {} got {}".format(short, verdicts[0], long_, verdicts[1]))
    record("allow", "every short option of _RG_ALLOW has a spelling pair row",
           set(s[1] for s, _l, _v in _RG_SPELLING_PAIRS) == set(_RG_ALLOW[0] + _RG_ALLOW[1])
           and all(l in (_RG_ALLOW[2] if v else _RG_ALLOW[3]) for _s, l, v in _RG_SPELLING_PAIRS)
           and all(s[1] in (_RG_ALLOW[0] if v else _RG_ALLOW[1]) for s, _l, v in _RG_SPELLING_PAIRS))
    # Round 32 (D-2385, D-2384): each exception and here-document row, with its rule in place and reverted
    for rule, command, expected in _RULE_CASES:
        got = _run_case(command)
        reverted_rules = (rule,) + (("simple command allowlist",) if rule in _ALLOWLIST_SUBSUMED_RULES else ())
        for name in reverted_rules:
            _RULES[name] = False
        try:
            reverted = _run_case(command)
        finally:
            for name in reverted_rules:
                _RULES[name] = True
        passed = got == expected and reverted != expected
        detail = "got {}, with {} reverted got {}".format(got, " and ".join(reverted_rules), reverted)
        if expected != ALLOW:
            flipped = _with_deny_logic_off(command)
            flip_checked += 1
            flip_passed += 1 if flipped == ALLOW else 0
            passed = passed and flipped == ALLOW
            detail += ", with the deny logic off got {}".format(flipped)
        record("rule-revert", "[{}] {}".format(rule, command), passed, detail)
    record("rule-revert", "every round 32 to round 35 rule has a row",
           set(r for r, _c, _e in _RULE_CASES) == set(_RULES))
    # Round 52 (grc review of round 50): a malformed payload denies as malformed input, not as an internal
    # error. Round 54 (grc review of rounds 51 to 53): the second row per case checks that the deny output
    # is a deny whose reason equals _REASONS[MALFORMED] and whose banner equals _BANNERS[MALFORMED] (which
    # shows the malformed-input message was chosen, but cannot catch a wrong text, as the code emits the
    # same constant), and that the reason holds the literal fragments "hook input was malformed" and "did
    # not evaluate any command" (which catch a reason text changed away from what it should say)
    for label, payload in _FAIL_CLOSED_CASES:
        got = _run_case(payload)
        flipped = _with_deny_logic_off(payload)
        record("fail-closed", label, got == MALFORMED and flipped == MALFORMED,
               "got {}, with the deny logic off got {}".format(got, flipped))
        obj = hook_output(got)
        hso = obj.get("hookSpecificOutput", {}) if isinstance(obj, dict) else {}
        reason = hso.get("permissionDecisionReason", "")
        record("fail-closed", "{}: malformed-input reason".format(label),
               hso.get("permissionDecision") == "deny"
               and reason == _REASONS[MALFORMED]
               and "hook input was malformed" in reason
               and "did not evaluate any command" in reason
               and obj.get("systemMessage") == _BANNERS[MALFORMED],
               "reason {!r}".format(reason[:120]))

    # An internal error denies, and the flip does not turn it into an allow.
    saved = globals()["_command_argvs"]

    def _boom(tokens):
        raise RuntimeError("injected internal error")

    globals()["_command_argvs"] = _boom
    try:
        got = _run_case("ls")
        flipped = _with_deny_logic_off("ls")
    finally:
        globals()["_command_argvs"] = saved
    record("fail-closed", "injected internal error", got == ERROR and flipped == ERROR,
           "got {}, with the deny logic off got {}".format(got, flipped))

    # Round 9 (qanorm8 finding 2): every $' is also a dollar-quote, so no command row can isolate the
    # $'...' NUL check; this row checks that it still reports its own construct.
    found = _unreadable_constructs(_Ctx(), "rm$'\\0' -rf x", [])
    record("detector", "the $'...' NUL check on its own", "a NUL from $'...' decoding" in found,
           "found {}".format(sorted(found)))

    # Output contract: the deny shape, and every fixed message but the malformed-input one names both
    # set-aside folders.
    shape_ok = True
    for decision in (DENY, CANNOT_PARSE, BROAD, ERROR):
        obj = hook_output(decision)
        hso = obj.get("hookSpecificOutput", {}) if isinstance(obj, dict) else {}
        shape_ok = shape_ok and sorted(obj) == ["hookSpecificOutput", "systemMessage"] and sorted(hso) == [
            "hookEventName", "permissionDecision", "permissionDecisionReason"] and hso[
            "hookEventName"] == "PreToolUse" and hso["permissionDecision"] == "deny"
        for text in (hso.get("permissionDecisionReason", ""), obj.get("systemMessage", "")):
            shape_ok = shape_ok and "/tmp/grc/deleteme" in text and "/tmp/deleteme-grc" in text
    record("contract", "deny output shape and set-aside folders in every message",
           shape_ok and hook_output(ALLOW) is None)
    # Round 52 (grc review of round 50): the malformed-input deny has the same shape, a reason and banner
    # of its own, and no file-removal advice (it names no set-aside folder)
    obj = hook_output(MALFORMED)
    hso = obj.get("hookSpecificOutput", {}) if isinstance(obj, dict) else {}
    record("contract", "malformed-input deny has its own plain reason and no file-removal advice",
           sorted(obj) == ["hookSpecificOutput", "systemMessage"]
           and hso.get("hookEventName") == "PreToolUse" and hso.get("permissionDecision") == "deny"
           and hso.get("permissionDecisionReason") == _REASONS[MALFORMED]
           and obj.get("systemMessage") == _BANNERS[MALFORMED]
           and "malformed" in _REASONS[MALFORMED] and "malformed" in _BANNERS[MALFORMED]
           and all(_REASONS[MALFORMED] != _REASONS[d] and _BANNERS[MALFORMED] != _BANNERS[d]
                   for d in (DENY, CANNOT_PARSE, BROAD, ERROR))
           and not any(s in text for text in (_REASONS[MALFORMED], _BANNERS[MALFORMED])
                       for s in ("deleteme", "set-aside", "removes files")))
    record("contract", "cannot-parse message says it denies in the safe direction",
           "safe direction" in _REASONS[CANNOT_PARSE] and "could not parse" in _REASONS[CANNOT_PARSE])
    # Round 13 (qanorm12 finding 4): the cannot-parse message names getattr and folded text as triggers
    record("contract", "cannot-parse message names getattr and NFKC folding",
           "getattr" in _REASONS[CANNOT_PARSE] and "NFKC folding" in _REASONS[CANNOT_PARSE])
    # Round 17 (qanorm16 F8): the short cannot-parse banner names NFKC folding too
    record("contract", "cannot-parse banner names NFKC folding", "NFKC folding" in _BANNERS[CANNOT_PARSE])
    record("contract", "deny message names git rm -f", "git rm -f" in _REASONS[DENY])
    # Round 15 (grc 0850 LOW 4): the cannot-parse message says how to pass text that holds a removal word
    record("contract", "cannot-parse message names git commit -F and grep -f",
           "git commit -F <file>" in _REASONS[CANNOT_PARSE] and "grep -f <file>" in _REASONS[CANNOT_PARSE])
    record("contract", "deny message names git clean", "git clean" in _REASONS[DENY])
    # Round 32 (D-2385): the broad-layer message says it refuses in the safe direction; round 34 (qanorm33
    # N7): neither the message nor the banner lists the places the broad layer exempts
    record("contract", "broad-layer message refuses in the safe direction and lists no exemption place",
           all(s in _REASONS[BROAD] for s in ("safe direction", "destructive git form")) and not any(
               s in text for text in (_REASONS[BROAD], _BANNERS[BROAD])
               for s in ("git commit -m or -F", "gh pr or gh issue", "gh pr or issue body", "grep or rg pattern",
                         "one of those places", "exempts")))

    # End to end: run this file as the hook, as the platform would.
    path = os.path.abspath(__file__)
    for label, stdin_bytes, want in (
            ("end-to-end deny", json.dumps(_bash("rm -rf x")).encode("utf-8"), DENY),
            ("end-to-end broad refusal", json.dumps(_bash("echo rm -rf x")).encode("utf-8"), BROAD),
            ("end-to-end allow", json.dumps(_bash("echo hello")).encode("utf-8"), ALLOW),
            ("end-to-end exception allow", json.dumps(_bash("git commit -m 'remove x'")).encode("utf-8"), ALLOW),
            ("end-to-end malformed payload", b"{", MALFORMED)):
        try:
            proc = subprocess.run([sys.executable, "-I", path], input=stdin_bytes, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, timeout=60)
            out = proc.stdout.decode("utf-8")
            if want == ALLOW:
                passed = proc.returncode == 0 and out == ""
            else:
                passed = proc.returncode == 0 and json.loads(out) == hook_output(want)
            detail = "exit {}, stdout {!r}".format(proc.returncode, out[:120])
        except Exception as exc:
            passed = False
            detail = "error {!r}".format(exc)
        record("end-to-end", label, passed, detail)

    # End to end: a deny that cannot be written (stdout is a pipe nobody reads) exits 2.
    try:
        read_fd, write_fd = os.pipe()
        os.close(read_fd)
        try:
            proc = subprocess.run([sys.executable, "-I", path],
                                  input=json.dumps(_bash("rm -rf x")).encode("utf-8"), stdout=write_fd,
                                  stderr=subprocess.PIPE, timeout=60)
        finally:
            os.close(write_fd)
        passed = proc.returncode == 2
        detail = "exit {}, stderr {!r}".format(proc.returncode, proc.stderr.decode("utf-8", "replace")[:160])
    except Exception as exc:
        passed = False
        detail = "error {!r}".format(exc)
    record("end-to-end", "deny that cannot be written exits 2", passed, detail)

    failed = [r for r in results if not r[2]]
    groups = {}
    for group, _label, passed, _detail in results:
        total, ok = groups.get(group, (0, 0))
        groups[group] = (total + 1, ok + (1 if passed else 0))
    for group, label, _passed, detail in failed:
        print("FAIL [{}] {!r}: {}".format(group, label, detail))
    print("self-test: {} cases, {} passed, {} failed".format(len(results), len(results) - len(failed),
                                                           len(failed)))
    for group in ("deny", "cannot-parse", "broad", "allow", "rule-revert", "fail-closed", "detector",
                  "contract", "end-to-end"):
        total, ok = groups.get(group, (0, 0))
        print("  {}: {} cases, {} passed".format(group, total, ok))
    print("broad layer: {} of {} allow rows refused (pinned {} by id)".format(
        broad_refused, len(_ALLOW_CASES), len(_BROAD_REFUSED_ALLOW_ROWS)))
    print("deny-logic flip: {} deny, cannot-parse and broad-refusal cases run with the deny logic off, {} of "
          "them allowed".format(flip_checked, flip_passed))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
