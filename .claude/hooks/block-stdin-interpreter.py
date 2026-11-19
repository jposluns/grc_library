#!/usr/bin/env python3
"""PreToolUse Bash hook: refuse an interpreter that reads its program from standard input.

Why: a program handed to an interpreter on standard input (``python3 -I - <<'EOF'``, a
here-string, a pipe, ``-`` or a process substitution) is not part of the command text, and
the command text is all a PreToolUse Bash hook reads, so no hook can check what that program
runs. Twice in one night ``python3 -I - <<'EOF'`` ran with an empty here-document: both ran
nothing, and nothing said so. A program written to a script file and run by its path is on
record and can be read back.

REFUSED (the interpreter and its arguments are read; a -c string and a here-document body
are never read as commands by these rules: a presence test on their text stands in, as
set out below, and the deny-by-default rule reads a listed shell's -c string as a line):
  * python, python3 and versioned names (python3.14, and the free-threaded python3t and
    python3.13t), by bare name or by path (/usr/bin/python3): ``-`` as the program (also
    after ``--``), or no script operand and no -c or -m.
  * perl, ruby, node and php (also nodejs and versioned perl, ruby and php names): ``-`` as
    the program, or no script operand and no inline program option.
  * bash, rbash, sh, zsh and dash: -s or +s (alone or in a cluster such as -xs or +xs), or no script operand while
    standard input is a here-document, a here-string, a pipe (also a pipe into a ( ) or { }
    group or into a while, until, for, select, if or case compound, a pipe continued past a
    newline or a comment after | or |&, a pipe into a command whose $( ) or backtick
    substitution runs the shell, since a substitution inherits the command's standard input,
    and the pipe a >( ) process substitution reads from the command it is written in, as in
    ``tee >(bash)``) or a process substitution (``bash < <(...)``). The script operand is the
    first word after the shell's options, skipped as for a -c string below: a cluster takes
    one word for each o or O in it, wherever the letter stands, so in ``cat /abs/run.sh |
    bash -ox pipefail`` pipefail is the argument of -o and no script operand is given.
  * a process substitution as the program: bash <(...), sh <(...), zsh and dash alike,
    source <(...) and . <(...) (also after ``--``), and any interpreter above given <(...) as
    its program, also when the substitution is written inside ${ } (``bash ${x:-<(...)}``).
  * a program path that names standard input: /dev/stdin, /dev/fd/0, /proc/self/fd/0.
  * a command name built by a glob or a brace expansion (an unquoted *, ? or [...], or a
    {...} holding a , or ..; also after the wrappers below), and a word one of the
    wrappers below reads as its option, option argument or operand so built, whatever the
    standard input is (``cat x | /bin/ba?h``, ``cat x | /bin/ba[s]h``, ``cat x |
    {,bash}``, ``/usr/bin/pyth?n3 -``, ``{,python3} -``, ``/b*/env bash -c 'cat x |
    bash'``, ``e[[:alpha:]]v bash -c 'cat x | bash'``, ``cat x | /b{in,in}/env cat``,
    ``/b*/nohup cat``). This hook does not expand the pattern and does not work out what
    it matches: a bracket expression may hold a character class, an equivalence class or
    a collating symbol, and a brace expansion may give any number of words, so any such
    name may name a wrapper, and any such wrapper operand may change which word is the
    command. Which command runs, and so how the words after it are read, is not known.
    Which of those characters were quoted is not kept, so a word holding one unquoted
    pattern character is read as a pattern throughout. Stated over-refusal: such a name
    that could name no listed interpreter or wrapper (``cat x | /abs/bin/fil?er``,
    ``/usr/bin/pyth?n3 -I /abs/script.py``, ``/bin/ba?h < /abs/run.sh``), a wrapper's
    name so built before a command the plain wrapper would be allowed to run
    (``/b*/env python3 -I /abs/script.py``, with or without ``<<< 'x'``), and a wrapper
    operand so built before such a command (``env -u H* python3 /abs/script.py``). A
    pattern in an argument of the command a line runs is not refused (``ls *.py | wc
    -l``, ``cat x | grep -e a*``).
  * a -c string given to bash, rbash, sh, zsh or dash, refused unread by a presence test on its text
    as the shell receives it and on that text with line continuations, backslashes and
    quotes dropped. A listed name is a listed interpreter, source or . written as a word, or
    as the part of a word after its last /, between blanks, newlines and the characters
    ; & | ( ) < > { } , and the backtick (also a listed interpreter, source or . standing
    alone in the text). Wherever this text uses a presence test for a listed name, a listed
    interpreter's name followed by a dot and more text also counts (``/abs/python.log``,
    ``bash.txt``, ``node.v2``): a stated over-refusal, so ``bash -c 'cat /abs/python.log |
    grep x'`` and ``cat /abs/python.log | a=1 while cat`` are refused. The string is
    refused when it holds $'...' or $"..." quoting; when
    it holds a listed name together with any of | < > ( [ { ' " or a backtick, so with a
    pipe, a redirection, a $( ), <( ) or >( ) substitution, an expansion, a group or a quote
    (``bash -c 'cat /abs/run.sh | bash'``, ``bash -c 'echo hi > >(bash)'``); or when a
    listed name in it is not followed by a script path:
    followed by a word that starts with - or + (an option, - or --) or by a path under /dev/
    or /proc/ (``bash -c 'python3 -'``, ``bash -c 'bash -s'``), or, for a listed interpreter,
    by nothing, a comment or a redirection before the next ; & | ( ) { } or newline
    (``bash -c 'python3'``; for bash, rbash, sh, zsh and dash only while the -c command's
    standard input is a here-document, a here-string, a pipe or a process substitution, as
    in ``cat /abs/run.sh | bash -c 'bash'``). A python name may have -I alone before its
    script path.
    Refused unread whatever the string names: a process substitution given as the string,
    and a string written in the command text with $'...' or $"..." quoting or an unquoted
    *, ?, [ or {. A string built by expansion (a $ form or a backtick the outer shell
    expands) is refused unread whenever it names a listed interpreter, source or . .
  * the body of a here-document whose delimiter is unquoted (``cat <<EOF``), refused unread
    when its text, or that text with line continuations, backslashes and quotes dropped,
    holds a $(, a ${, a $[ or a backtick together with a listed name as above (``cat <<EOF``
    with ``$(cat /abs/run.sh | bash)`` in the body), whatever stands around them.
  * an assignment prefix followed by a reserved word. After an assignment bash reads a
    reserved word (!, if, then, else, elif, fi, case, esac, for, select, while, until, do,
    done, in, function, coproc, {, }, [[ or ]]), quoted or not, as a command's name, so
    ``cat x | a=1 while bash`` runs a command named while, not a loop, and a NAME[ after
    that word is a plain word, so an operator after it ends the command. The word is read
    as bash reads it once the quoting is removed: single or double quotes, a backslash, a
    line continuation, $"..." (read as its text), $'...' with every escape decoded as bash
    decodes it (\\a to \\v, \\nnn, \\xHH, \\x{H...}, \\uHHHH, \\UHHHHHHHH and \\cX, \\cX from the
    first byte of X's UTF-8 encoding with X's other bytes kept, as bash does, never from an
    uppercase form of X; a NUL ends that $'...' segment; an escape bash does not decode
    (a character after the backslash with no escape meaning, \\x, \\u or \\U with no digit,
    or \\c at the end of the quote) is kept as bash keeps it, a backslash followed by that
    character, so ``echo $'\\q'`` and ``grep -P $'\\d+\\t' /abs/f`` are allowed and ``cat x
    | a=$'\\q' bash`` is refused by the shell rule; a \\U value above 10FFFF is refused as
    a parse failure, below), and any mix of them (``cat x | a=1 $'wh\\x69le' bash``, ``a=1
    $'wh\\0zz'ile``, ``a=1 "w"$'\\x68'i\\le``). The rule, fail closed: in a command line
    that feeds standard input to an interpreter, an assignment prefix followed anywhere
    later in the same simple command by such a reserved word in command position is
    refused, whatever words, subscripts, operators or redirections sit between or after
    (``cat x | a=1 3>out while b[ 0 ]=2 bash /abs/run.sh``, ``a=1 while b[ ; cat
    /abs/run.sh | bash ; ]=2 cat``). The rule applies in every nested command context: in
    a $( ), backtick, <( ) or >( ) substitution written in any word or in a redirection's
    target, at any depth (``echo x > >(a=1 while b[ 0 ]=2 bash)``, ``cat x | a=1
    >"$(a=1 while b[ 0 ]=2 bash)" cat``). Read so that no subscript spelling hides it: an
    assignment prefix is an assignment word, or a word that begins NAME[, after a command's
    leading shell words (time -p, time -- and time -p -- among them, as bash reads them);
    after it every word counts as in command position; and while a [ in a word after it
    is still open, an operator or a newline does not end the simple command, since a
    subscript may hold one (``cat x | a=1 3>out b[ ; ]=2 while bash``).
    A command line feeds standard input to an interpreter when its text, or that text with
    line continuations, backslashes and quotes dropped, names a listed interpreter, source
    or . (as for a -c string above) and holds a |, a <, a >( or a word that is - or a
    standard-input path, or when a later word of such a simple command, read as a
    command's start, is refused by the rules above (``a=1 while b[ 0 ]=2 python3``). The
    refusal gives that later word's reason when there is one. Stated over-refusals: ``cat
    x | a=1 while bash /abs/run.sh``, ``cat x | a=1 echo while bash`` (also ``cat x | a=1
    time while bash``: bash runs time there as a command, not as its shell word, and the
    rule reads it as any other word between), and a listed name
    that is only an argument (``cat x | a=1 while echo bash``, where bash runs a command
    named while). The last is accepted: the textual test refuses it whatever the later
    words are read as, so reading only the words after the reserved word as a command's
    start would not allow it, and would give up the later-word reading that refuses
    ``a=1 while b[ 0 ]=2 python3``. How far this reaches into ordinary search commands:
    the reserved word need not stand where bash reads a command, and the line need not
    run any interpreter. An environment prefix before a search command whose pattern or
    name argument is a reserved word, quoted or not, is refused, a stated over-refusal,
    whenever any word of the line names a listed interpreter, source or . as the textual
    test above reads it (a . path argument, a path such as /abs/bash or /abs/sh.txt, or a
    later pipeline stage such as grep -c bash) and the line holds any feed that test reads
    (a pipe, a here-string, a here-document or another <): ``LC_ALL=C grep -rnw in . |
    head``, ``LC_ALL=C grep -rw "if" . | head``, ``NO_COLOR=1 rg -w done . | head -5``,
    ``LC_ALL=C find . -name for | sort``, ``LC_ALL=C grep -rw do /abs/bash | head``,
    ``LC_ALL=C grep -rw if /abs/src | grep -c bash``, ``GREP_COLOR=1 grep -w then
    /abs/sh.txt | head``, ``LC_ALL=C grep -rw in . <<< x``. The same search is allowed
    with no assignment before it (``grep -rnw in . | head``), with an absolute path in
    place of . when no other word names a listed interpreter, source or . (``LC_ALL=C
    grep -rnw in /abs/src | head``), or with no feed (``LC_ALL=C grep -rnw in .``). Not
    refused: a line
    naming no listed interpreter, source or . (``cat x | a=1 while cat``), or one with no
    such feed (``a=1 while bash``, ``a=1 if python3 -I /abs/script.py``). Each simple
    command is also read as bash reads it: the reserved word is skipped and the next word
    read as the command, so the rules above refuse ``a=1 while python3 -`` as at a
    command's start. time after an assignment is read through the time wrapper, and a word
    that only an expansion supplies is not read as a reserved word.
  Every simple command is checked: after ;, &&, ||, |, &, a newline or a ( ) or { } group,
  inside $( ), backticks, <( ) and >( ) (also a $( ) or backticks written inside ${ }, $(( )),
  (( )) or $[ ], a <( ) or >( ) written unquoted inside ${ }, and any of them written in an
  array assignment's list, as in ``a=($(...))``, each read with the standard input of the
  command it is written in), behind leading assignments (array assignments such as
  ``a=(1 2)`` and subscripted ones such as ``a[ 1 ]=1`` or ``a[$i]=1`` included: a NAME[
  where an assignment may stand is read to its matching ], blanks, quotes, operators and
  expansions included, as bash reads it), behind the shell words !, time (with -p, --, or
  -p then --, which bash skips after it, so ``time -- python3 -`` is refused), if, then,
  else, elif, do, while, until and coproc before any assignment (after one, by the rule above
  for an interpreter after a leading assignment that leaves a reserved word in command
  position) (and a coproc's NAME before a compound command, so
  ``coproc NAME { ...; }`` is read as ``coproc { ...; }``), and behind the wrappers env (with
  -i, -u, -C and -S, also in a cluster such as -iC DIR, where u, C or S takes the rest of the
  word or else the next word), command (-p), exec (-a, -c, -l, also in a cluster such as
  -ca NAME), nice (-n and -N), timeout (-s, -k and the duration), nohup, sudo (its options
  read from its full option table: -a, -C, -c, -D, -g, -h, -p, -R, -r, -T, -t, -U and -u
  take an argument, also in a cluster such as -Eu NAME, by the same rule as env, and so do
  their long forms, as --user=NAME or --user NAME; a long option written as a prefix of
  exactly one of sudo's long names is read as that option, as sudo's getopt_long reads
  it, so --us NAME is --user NAME) and /usr/bin/time, each with its
  options. After env's options, and
  after sudo's, every operand that holds an = is read as NAME=VALUE and skipped, whatever
  its name, as GNU env reads it (``cat x | env a-b=1 bash``, ``cat x | env '\\q'=1 bash``
  and ``cat x | sudo $'\\q'=1 bash`` are refused), so the command is the first operand
  without an =.
  * a command fed standard input whose command word cannot be determined with certainty.
    A simple command is fed standard input when it is a listed shape (a here-document, a
    here-string, a pipe or a process substitution) or a word of it is -, a standard-input
    path or a process substitution. Where the hook reads such a command's command word,
    it refuses the command, naming the reason, rather than guess, when: a word in command
    position, or a word a wrapper reads as its option, option argument or operand, is not
    literal text (any $ expansion, $( ) or backtick substitution, $(( )), or a glob or
    brace expansion: ``cat x | $V bash``, ``cat x | a=1 $(true) bash``, ``cat x | env
    "$(printf a=1)" python3``, ``cat x | env $V python3 -``, ``cat x | sudo $(echo a=1)
    bash``); env -S text holds a backslash, a $, a # or a vertical tab or form feed: GNU
    env reads a backslash as an escape, a $ as a variable reference and a # as a comment,
    and outside quotes it splits on a vertical tab or a form feed as on a blank, and this
    hook does not split such text as GNU env does (``printf 'echo QA_OK\\n' | env -S
    $'a-b=1\\_bash'``, ``cat x | env -S '#x' bash``, ``cat x | env -S '${SHELL}'``); a
    sudo short option is not in sudo's option table, so whether it takes the next word is
    not known (``cat x | sudo -z nobody bash``); a sudo long option that takes no argument
    is given one after an = (``cat x | sudo --shell=x bash``): the = means it takes no next
    word, but the table says it takes no value, so the line is refused as one the table
    does not describe rather than read; a sudo -h has nothing
    attached (as a word of its own or ending a cluster), which sudo's manual lists both
    as its help option and as its host option, so whether it takes the next word is not
    known (``cat x | sudo -h bash``, ``cat x | sudo -h host bash``; ``cat x | sudo -hhost
    tee /abs/out``, ``cat x | sudo --host=host tee /abs/out`` and ``cat x | sudo --help
    tee /abs/out`` are allowed); or a sudo NAME=VALUE
    operand is followed by an option-shaped operand, which sudo reads after it has
    stopped reading options (``cat x | sudo a=1 -u nobody bash``).
    Wrappers nested more than 16 deep are refused whatever the standard input is (``cat x
    | `` and 17 ``nohup`` words before ``bash``), and so is a sudo long option that is
    neither one of sudo's long names nor a prefix of exactly one of them, which sudo's
    getopt_long reads as an abbreviation, since whether it takes the next word is not
    known (``sudo --frobnicate nobody bash -c 'cat x | bash'``, ``cat x | sudo
    --frobnicate nobody bash``, ``sudo --log nobody tee /abs/out``, --log being a prefix
    of --login and of --login-class). This is a deliberate over-refusal: the
    rule does not ask whether the word could name an interpreter, so it refuses ordinary
    commands too (``cat x | $PAGER``, ``cat x | sudo -u "$USER" tee /abs/out``, ``cat x |
    env -S 'grep -e a\\tb'``, ``cat x | sudo a=1 -E tee /abs/out``, a sudo long option
    abbreviated to a prefix of more than one long name, as in ``cat x | sudo --log nobody
    tee /abs/out`` (``cat x | sudo --us nobody tee /abs/out`` is allowed), a sudo -h with nothing attached before a literal command, as in ``cat x |
    sudo -h host tee /abs/out`` and ``cat x | sudo -h``, 17 ``nohup`` words before
    ``echo hi``), and, in a pipe, a loop or
    condition word supplied by an expansion
    (``cat x | while $RUNNING; do ...``). An expansion in an argument of a literal
    command is not refused (``cat x | grep "$(date +%Y)"``), nor is a command fed no
    standard input (``echo $V``, ``$V bash``). An arithmetic command, (( )) at a command's
    start or after a shell word such as do, while or {, runs no command, so it is neither
    refused nor read as a command word (``cat x | (( 1 ))``, ``cat x | while (( $# )); do
    shift; done``, ``cat x | { (( $n )); }``, ``cat x | while read -r n; do (( $n > 5 ))
    && echo big; done``). A substitution inside it and every command after it are read as
    anywhere else (``cat x | (( $(bash) ))`` and ``cat x | while (( 1 )); do bash;
    done`` are refused); with a further word in the same simple command, which bash
    rejects, it is read as an expansion in command position (``cat x | (( 1 )) bash`` is
    refused). A (( is an arithmetic command only as bash reads one: the ) that matches its
    second ( is followed at once by ) (``cat x | (( (1) ))`` is allowed). Otherwise bash
    reads a subshell holding subshells and runs their commands, and so does this hook
    (``cat x | ((true) && (bash))``, ``cat x | ((:);(bash))`` and ``cat x | (((:));(bash))``
    are refused); the same holds for $(( )) and a command substitution. Where a quote,
    backslash or backtick, or a comment or case in a substitution, comes before that ) is
    found, the reading cannot be settled and the text is refused as unreadable. Only a
    substitution's own text is read for a comment or case: a # that starts a word, and a
    case word where bash reads a command's first word (``(( $(case x in x) echo 1;; esac)
    ))`` is refused); a # inside a word and case inside a word or as an argument are
    neither (``(( 16#ff + $(echo 1) ))``, ``(( $(echo 16#ff) ))`` and ``(( testcase +
    $(echo 1) ))`` are allowed).
  A {NAME} word written directly before a redirection operator that starts with < or >
  (``{fd}>/dev/null``, ``{fd}<o``, also ``{NAME[...]}``) is read as that redirection's
  descriptor, as bash reads it (bash opens a new descriptor and stores its number in NAME),
  wherever it stands: at a command's start, between assignments and after the command's
  name, so ``cat x | {fd}>/dev/null bash`` and ``cat x | a=1 {fd}>o b=2 bash`` are read as
  bash reading a pipe, and a substitution in its subscript is read as in any word. The word
  is matched on its text once quoting is removed, so a quoted ``'{fd}'>o``, which bash reads
  as a word, is read as a descriptor too: a stated over-refusal (``cat x | '{fd}'>o bash``
  is refused though bash runs a command named {fd}).

DENY BY DEFAULT. The rules above read the constructs this hook's reader models, and every
earlier version of that reader has met a shell construct it did not model (a while form
after an assignment, an array subscript, a redirection between words, a substitution
nested in another, a $'...' escape, a {NAME} descriptor, a glob or brace form, an extended
pattern such as @( )). So, once the rules above allow a line, a last rule reads the line
again on its own, quote by quote, and refuses it as cannot-determine, never allows it,
when a command that receives a feed meets the test below. Only that command is read: a $,
a pattern or an interpreter's name elsewhere on the line does not meet the test.
  * The commands that receive a feed: the command after a | or |& (also past a newline);
    the command that a here-document, a here-string, a < redirection (by any descriptor,
    00< and {NAME}< included, and <& and <>) or a <( ) process substitution written in it
    feeds; every command inside a >( ) process substitution; every command of a group or
    compound a pipe feeds (a { } or ( ) group, a function definition, and a while, until,
    if, for, select or case compound), read to the closing word that matches it, or, for
    a ( ) group and a case compound, to the end of the text it stands in; every command of
    a level in which a group, a compound or an exec of redirections is given a <
    redirection (``done < /abs/list``, ``exec < <(cat /abs/run.sh)``); and every command
    inside a $( ), backtick, <( ) or >( ) substitution written in a command that receives
    a feed or in the body of a here-document it reads. Quotes, $( ), ${ }, $(( )), $[ ],
    backticks, [[ ]] and here-document bodies are read to their ends (a body whose
    delimiter is unquoted is read for substitutions), so a < or | inside a quote, in
    $(( )) or in [[ ]] is not a feed (``echo $((1 << 2))``, ``cat x | grep 'a|b'``).
  * The command word of such a command is the first word after its assignments, its shell
    words (!, time, if, then, else, elif, do, while, until, {, coproc and the closing
    words) and the wrappers env, command, exec, nice, timeout, nohup, sudo, time, xargs,
    stdbuf, setsid, ionice, flock (its options, then its lock file), busybox and builtin,
    each with its options read as for the rules above (xargs: a, d, E, I, L, n, P and s
    take an argument, and --max-lines, whose argument must be attached, takes none;
    stdbuf: i, o and e; ionice: c, n, p, P and u; flock: E and w). eval joins its
    operands and bash reads them again as shell text, so they are read as a line of their
    own in which every command receives the feed (``cat x | eval 'true; bash'``); a flock
    -c string is read the same way, and a flock -c written among its options is refused
    as unlocated. A command word that names a function the line defines is read through
    that function's body, every command of it receiving the feed, with a variable in it
    resolved against the line (``f() { bash; }; cat x | f``).
  * The line is refused when, for such a command: its command word, or a wrapper's name,
    option, option argument or operand before it, can build a word at run time: a $ in
    any form, quoted or not, a backtick, or, unquoted and not after a backslash, a glob
    character (* or ?), a bracket expression, a brace pattern or an extended pattern (?
    * + @ or ! directly before a (, read as part of its word) (``cat x | eval "$SHELL"``,
    ``cat x | xargs /bin/ba?h``, ``cat x | timeout $T cat``, ``cat x | env A=1
    py{thon3,}``); its command word or a wrapper's name lies outside the modelled set
    below (``cat x | ~/bin/tool``), an assignment before it has a subscript (``cat x |
    a[0]=1 cat``), or it is an arithmetic command that names a listed interpreter, holds
    a $( or backtick substitution or has a further word (a $NAME, a $# or a +( in one
    builds no word: ``cat x | ((1+(2)))`` is allowed); its command word is a listed
    interpreter, source or . given no literal program operand (no script operand, -, a
    standard-input path or -s, and no path under /dev/fd/ or /proc/*/fd/ or naming
    /dev/std*, in any spelling: ``cat x | bash /dev/fd/3 3<&0``, ``python3 //dev/stdin
    <<<'print(1)'``), unless its only
    feed is a < redirection from a named file, as below (``bash 00<<<'echo hi'``, ``cat x
    | { cat; bash; }``, ``cat /abs/a | diff <(bash) /abs/b``, ``cat x | tee
    >(python3)``); or its command word is a listed interpreter, source or . and a word
    that chooses its program lies outside the modelled set: the command word, a {NAME}
    descriptor, the interpreter's options and its program operand (the script path, or
    the word after -c, -e or -m), and, with no program operand, every word, redirection
    target and unquoted here-document body of the command (``cat x | python3 -I "$S"``,
    ``cat x | {fd}>/dev/null python3 -I /abs/s.py``). A program operand that is only a
    variable ($NAME, ${NAME} or "$NAME") is read as its value when the line sets it
    exactly once, before its first use, by an assignment whose value is literal text of
    the modelled set that does not start with - and names no standard-input path, the
    name appears nowhere else outside quotes and here-document bodies, and the line holds
    no eval, source or . (``T=/abs/tool.py; printf %s "$X" | python3 -I $T --append`` is
    allowed); and only when that assignment is a simple command of its own at the top
    level of the shell: not a prefix to a command word, not in a ( ), $( ), backtick,
    group, compound or function, not a pipeline stage, not after && or || and not in the
    background (``T=/abs/s.py true;``, ``(T=/abs/s.py);`` and ``false && T=/abs/s.py;``
    before ``cat x | python3 -I $T`` are refused; so, a stated over-refusal, is ``cd /abs
    && T=/abs/s.py;`` before it). The words
    after a literal program operand are the program's arguments and are not read
    (``python3 -I /abs/s.py --id "$ID" < /abs/in.txt`` is allowed).
  * A line in which the commands that receive a feed cannot be located (an unterminated
    quote, substitution or extended pattern, a redirection with no target, a pipe with
    nothing after it, nesting deeper than MAX_DEPTH) is refused. So is a line holding a
    command whose command word can build a word at run time when a quoted argument of it,
    read as a command line of its own (it may be a shell's -c program), is refused by
    this rule (``$SH -c "cat x | bash"``). The -c string of a listed shell (bash, rbash,
    sh, zsh or dash, also past the wrappers above), eval text and a flock -c string are
    read as a line of their own: with the feed the command receives, every command of it
    receiving that feed, or as they stand when it receives none (``bash -c 'cat
    /abs/run.sh | /bin/ba?h'``, ``cat x | bash -c 'env -Spython3'``, ``cat x | xargs sh
    -c bash``).
  The modelled set is: words made only of ASCII letters, digits and _ . / : = @ % + , - ;
  blanks and newlines; the operator characters | & ; < and > ; a single-quoted string; a
  double-quoted string holding no $, backtick or backslash; and a here-document whose
  delimiter is such a word, quoted string or word with a backslash before a character,
  with a body that is never read when the delimiter is quoted and that holds no $,
  backtick or backslash when it is not. The test command [ is read as a literal command
  word.
  Stated over-refusals: a command word outside that set that runs no interpreter (``cat x
  | ~/bin/tool``, ``cat x | a[0]=1 cat``); an interpreter that receives a feed and is
  given a program operand built at run time that the line does not set as above, or that
  holds a word outside the set before it (``cat x | python3 -I "$S"``); every command of
  a ( ) group or a case compound after a pipe, to the end of the text, and every command
  of another compound to its matching closing word (``cat /abs/a | for i in 1; { :; };
  bash``, ``cat /abs/a | case x in x) :;; esac; bash``); every command of a level in
  which a group, a compound or an exec of redirections is given a < redirection; and a <
  redirection by any descriptor, which is counted as a feed. Not refused: a $, a pattern,
  an expansion or an interpreter's name in an argument of a command whose command word is
  literal and not an interpreter (``printf %s "$(date)" | wc -c``, ``cat x | grep
  "$(date +%Y)"``, ``ls /abs/*.py | wc -l``, ``cat x | env LC_ALL=C grep -e "$P"``, ``cat
  x | grep -c bash``); an arithmetic command or expansion that names no interpreter and
  builds no word (``cat x | (( count++ ))``, ``cat x | echo $(( (1) + (2) ))``); an
  interpreter that receives a feed and is given a literal script path (``echo hi | tee
  >(bash /abs/run.sh)``, ``cat x | bash /abs/run.sh "$l"``); a here-document body
  substitution that runs no interpreter (``cat <<EOF`` with ``$(date)`` in the body); and
  an interpreter given no program operand whose only feed is a < redirection from a named
  file (``while read -r l; do bash; done < /abs/list``), as ``bash < /abs/run.sh`` is
  allowed below.
  Where the text above or below calls a line allowed or a residual gap and this rule
  refuses it, the earlier text describes only how the reader reads it: a piped function
  definition in either form (``cat /abs/run.sh | foo() { bash; }``), a command after a
  piped for or case compound (``cat /abs/a | for i in 1; { :; }; bash``), a piped array
  assignment then a shell (``cat /abs/run.sh | a=()`` then ``bash``), a shell in a <( )
  process substitution in a piped line (``cat /abs/a | diff <(bash) /abs/b``), ``bash
  00< <(cat /abs/run.sh)``, ``bash 00<<<'echo hi'``, ``exec < <(cat /abs/run.sh);
  bash``, a subscript after a redirection (``cat /abs/run.sh | a=1 3>/dev/null b[ 2 ]=2
  bash``) and a {NAME} descriptor before a shell given a script (``cat x | {fd}>/dev/null
  bash /abs/run.sh``); and the same lines where a variable, an expansion or a pattern
  supplies the name (``cat /abs/a | diff <($BASH) /abs/b``, ``b${x}ash 00< <(cat
  /abs/run.sh)``, ``exec < <(cat /abs/run.sh); $BASH``, ``cat x | eval b${x}ash``).

ALLOWED:
  * the same interpreter given a script path (python3 -I /abs/script.py, bash /abs/run.sh),
    whatever its standard input is.
  * a program given inline or by name: python -c and -m, perl -e and -E, ruby -e, node -e,
    --eval, -p and --print, php -r, -R, -B, -E, -f and -F. Those stay with their own hooks'
    rules and are out of scope here. A -c string for bash, rbash, sh, zsh or dash is allowed when
    the presence test above does not refuse it: it names no listed interpreter, source or .
    (``bash -c "echo hi"``, ``cat x | sh -c 'grep y'``, ``bash -c "echo $HOME"``), or it has
    no $'...' or $"..." quoting, none of | < > ( [ { ' " and no backtick, and each listed name
    in it is followed by a script operand (``bash -c 'python3 -I /abs/s.py'``, ``cat x | bash -c
    'bash /abs/run.sh'``), or is source or . with nothing after it, or is bash, rbash, sh,
    zsh or dash with nothing after it while the -c command's standard input is none of
    the listed shapes (``bash -c 'bash' < /abs/run.sh``).
  * a here-document whose delimiter has a quote or a backslash in it (<<'EOF', <<"EOF"),
    whatever its body holds, and one with an unquoted delimiter whose body holds no $(, ${,
    $[ and no backtick, or names no listed interpreter, source or . (``cat <<EOF`` with
    ``$(date)`` in the body).
  * an informational call that reads no program (--version, -V, --help, -h and the like).
  * bash, rbash, sh, zsh or dash with no script operand and no listed standard-input shape (a bare
    ``bash``), or with standard input redirected from a named file (``bash < run.sh``): the
    shell rule names here-documents, here-strings, pipes and process substitutions only.
  * any other command reading a here-document, a here-string or a pipe (cat <<'EOF'),
    when its command word and every word its wrappers read are literal text: ``cat x |
    grep bash``, ``printf %s "$(date)" | wc -c``, ``cat x | grep "$(date +%Y)"``, ``cat
    x | env LC_ALL=C sort``, ``cat x | sudo -u nobody tee /abs/out``, ``cat x | env -S
    'sort -u'``, and 16 nested ``nohup`` words before ``grep y`` in a pipe; and a command
    fed no standard input, whatever its words (``echo $V``, ``env a=1 printenv``).
  * a function definition, piped or not, in either form (``function foo { bash; }`` and
    ``foo() { bash; }``), also after shell words (``do foo() { bash; }``, ``then foo() {
    bash; }``) and inside a group: its body runs when the function is called, not under the
    pipe. An assignment whose value is a parenthesized list (``a=()``, ``a+=(x)``,
    ``a[0]=(x)``) is read as one assignment word, never as a word and a ( ) group, so it never
    starts a definition; nor does a word that is not a function name this hook reads
    (letters, digits, _, ., : and -).
  * an array assignment's elements, which are words, not commands (``a=(python3)``).
  * a reserved word after an assignment in a command line that the rule above for an
    assignment prefix followed by a reserved word does not refuse (``cat x | a=1 while
    cat``, ``a=1 while bash`` with no standard-input shape).

PARSE FAILURE. In the command text this hook parses, which is everything outside a -c
string and a here-document body, an unterminated quote or substitution, an unclosed
group, a NAME[ subscript with no matching ], a here-document operator with no delimiter,
a redirection with no target, nesting deeper than MAX_DEPTH, or a $'...' escape this
reader does not decode (a \\U value above 10FFFF, for which bash writes bytes this reader
does not model, or any error while decoding; an escape bash itself does not decode is
kept as bash keeps it, above) is always refused, with its own message (``echo "a``). That
parse does not enter a -c string or a here-document body, and a parse failure inside one
is decided as follows:
  * a here-document body whose delimiter has a quote or a backslash in it is never read,
    so a parse failure in it is allowed (``cat <<'EOF'`` with ``${x`` in the body).
  * a here-document body whose delimiter is unquoted is refused when its presence test
    refuses it, and also when the deny-by-default rule cannot read a $( ), ${ }, $[ ] or
    backtick substitution in it to its end (``cat <<EOF`` with ``$(echo`` in the body).
    Any other parse failure in it, such as an unpaired quote, is allowed.
  * a listed shell's -c string is refused when its presence test refuses it (``bash -c
    'python3 "a'``). That string, eval text and a flock -c string are also refused when
    the deny-by-default rule, reading the text as a line of its own, cannot locate a
    command in it that receives a feed: the text holds a |, a < or a >( (``bash -c 'cat x
    | echo "a'``), or the shell, eval or flock itself receives a feed (``cat x | bash -c
    'echo "a'``). Any other parse failure in such text is allowed (``bash -c 'echo "a'``,
    ``eval 'echo "a'``).
The existing hooks have no single convention to follow (block-verification-pipes
refuses shapes it cannot read, block-bulk-git-add allows a tokenizer failure), so this hook
takes the closed side. A malformed payload or a non-Bash tool call FAILS OPEN, as in every
existing hook. An unexpected error anywhere in reading the command text FAILS CLOSED: the
line is refused, with the error's type named, since a reader that stops part way has not
shown that the line is safe.

No _hookutil helper fits: strip_heredocs keeps unquoted bodies and matches a terminator after
strip(), and command_word reads ``timeout -s KILL 5 cmd`` as ``KILL``. This hook carries its
own reader, standard library only, and loads no repository helper. Import isolation
depends on the launch line: settings.json starts the hook as /usr/bin/python3 -I, which
leaves the hook's own directory off sys.path, so a module beside it with the name of a
standard module the hook imports (a shlex.py or json.py in .claude/hooks) is not imported
in its place. The hook does not isolate sys.path itself: started without -I, Python puts
that directory first on sys.path and such a module would be imported, so run the hook,
its self-test included, under python3 -I.

RESIDUALS, stated because they are real gaps:
  * standard input redirected from a file, including a file the same command writes: a shell
    is allowed to read a named file (``cat > gen.sh <<'EOF' ... EOF`` then ``bash < gen.sh``),
    and ``python3 - < gen.py`` after ``cat > gen.py`` is refused only by the ``-`` rule; the
    file's content is never read.
  * a program fetched or built at run time and then run by path (download x.py, then python3
    x.py), an interpreter's operand that only a variable or a substitution supplies
    (python3 "$(echo -)"), and a command word that only a variable or a substitution
    supplies in a command fed no standard input (``$PY`` with no feed, which then reads
    the terminal); one in a command fed standard input is refused, above.
  * interpreters outside the list (ksh, fish, pypy, lua, Rscript and others) and wrappers
    outside the list (doas, script, ssh, chroot, unshare and others). The rules above read
    env, command, exec, nice, timeout, nohup, sudo and time as wrappers; xargs, eval,
    stdbuf, setsid, ionice, flock, busybox and builtin are read only by the
    deny-by-default rule, so only in a command that receives a feed, and eval text, a
    flock -c string and a shell's -c string also as a line of their own.
  * a command placed in a script file, or started by a subprocess, an eval or a remote shell:
    the route residue every command-text hook here discloses.
  * the rules above do not carry a pipe into a function called later into its body (the
    deny-by-default rule does, for a function the same line defines): a function definition
    (``function NAME {`` or ``NAME() {``) never opens its body under a pipe. A function name
    bash accepts outside the set above (``f+x() { ...; }``) is read as a command and a ( )
    group, not as a definition. A group or compound is opened only by its keyword at the start
    of a command (after nothing but the shell words above); a for or select head ends at the
    first unquoted do at a command start, or at do right after NAME when there is no in list
    (``for i do``); its body written as { } is read as the body only when { starts the first
    command after the head; and a closing word (}, done, fi, esac) closes only the innermost
    open entry it matches; a case pattern's ) never closes a ( ) group.
  * a <( ) process substitution, unlike $( ) and backticks, is never treated as reading the
    pipe into the command it is written in (the rules above allow ``cat x | diff <(bash)
    y``; the deny-by-default rule refuses it), except in
    an array assignment's list, where it keeps the command's standard input as bash runs it
    (``cat x | a=(<(bash))`` is refused). A >( ) one is always read as standard input from a
    pipe, whatever the command writes to it.
  * a word is read as an array assignment when an unquoted NAME=, NAME+= or NAME[i]= in it is
    followed directly by (, wherever the word stands; bash accepts that only where an
    assignment may stand (``echo a=(x)`` is a syntax error there). An operator other than a
    newline inside the list fails closed; bash rejects it too, except inside an element's
    [ ] subscript (``a=([;]=x)`` is refused though bash accepts it).
  * an unquoted NAME[ is read to its matching ] as one word (blanks, quotes, operators and
    expansions inside it, the brackets nested) only where bash reads it so, as observed with
    bash 5.3: at a command's start, after the shell words above, after an assignment, and
    after redirections written before any word; after a redirection that follows a word or
    an assignment, after a reserved word that follows an assignment (bash 5.3.9 runs the
    text after ; in ``a=1 while b[ ; echo x ; ]=2 true``), and anywhere else, [ is a plain
    character, an operator after it ends the simple command as bash reads it, and the word
    is still an assignment when an unquoted NAME[...]= begins it. Where an assignment
    prefix is followed by a reserved word, the rule above for that form reads an open [
    as holding the operators after it, for failing closed only. Where bash sets that position by rules
    this reader does not model (after a coproc's or a function's NAME, a case pattern after
    (, time -p after a pipe, where bash runs /usr/bin/time and not the shell word) the word
    may be split differently from bash: ``cat x | time -p a[ 1 ]=1 bash`` is refused though
    bash runs /usr/bin/time on the command a[.
  * a coproc's own pipe is not read as a standard-input shape: ``coproc { bash; }`` is allowed
    unless the coproc is itself written under a pipe, and a later command that writes to the
    coproc's descriptor is not linked to it. The word after coproc is read as the coproc's
    NAME only before a compound command ({ }, ( ), while, until, for, select, if or case);
    before anything else it is read as the command (``coproc MYPROC sleep 1`` is read as the
    command MYPROC with the arguments sleep and 1).
  * inside ${ }, $(( )), (( )) and $[ ], a $( ), backtick, nested ${ } or nested $(( )) is
    read as anywhere else, and its command keeps the standard input of the command the
    expansion is written in. Inside ${ }, an unquoted <( ) or >( ) (in any part of the body,
    a pattern included) is read as a process substitution by the rules used elsewhere, and
    the word holding it is read as a process substitution where it stands as a program, a
    sourced file or a < target, even when the parameter is set and bash would expand its
    value instead (``bash ${x:-<(...)}`` is refused whatever x holds); one inside double
    quotes is text, as bash reads it. Quoting inside an arithmetic body is not modelled (a
    quote there is a plain character); the end of $(( )) and (( )) is found by counting
    parentheses and the end of $[ ] at the first ], so a (, ) or ] inside a quote in them can
    end the expression early: the rest is then read as command text, or the text is refused
    when a substitution runs past the end. A quote, backslash or backtick before the ) that
    matches the second ( of (( or $(( makes the text unreadable (refused), even where bash
    would read plain arithmetic (``cat x | (( x == "1" )) && bash`` names an interpreter and
    is refused as unreadable): a stated over-refusal.
  * sudo's option table is the one in sudo's manual (sudo(8), upstream at
    https://www.sudo.ws/docs/man/sudo.man/, read 2026-11-17); an option a later sudo adds
    is refused while it is not in the table, as above. A command fed no standard input
    reads a short option outside the table as taking no argument, and -h with nothing
    attached as taking the next word (a host name); a long option outside the table, or a
    prefix of more than one long name, is refused in any command. --preserve-env as a word of its own is read as
    taking no argument, as the manual's -E, and its list only after an =.
  * by the rules above, a -c string (bash, rbash, sh, zsh and dash only) and an unquoted
    here-document body are never read as commands: the presence tests above stand in for
    that and do not tell a command from text, a substitution from an escaped one, or which
    standard input a command has. The deny-by-default rule reads a listed shell's -c
    string as a line of its own (above), so some lines these tests allow are refused there.
    Over-refusals, each refused whatever it runs: in a -c string, a listed name together
    with any of | < > ( [ { ' " or a backtick (``bash -c 'echo $(python3 /abs/s.py)'``,
    ``bash -c 'python3 /abs/s.py > /abs/out'``, ``bash -c "python3 '/abs/a b.py'"``); in an
    unquoted body, a listed name together with a $(, ${, $[ or backtick (``cat <<EOF`` with
    ``$(python3 /abs/s.py)``, with an escaped ``\\$(cat /abs/run.sh | bash)`` or with
    ``python3 at ${HOME}`` in the body); in a -c
    string, $'...' or $"..." quoting anywhere (``bash -c 'echo $"hi"'``), and a listed name
    not followed by a script path in the forms above, as text or as an argument (``bash -c
    'echo python3'``, ``bash -c 'python3 -u /abs/s.py'``, ``bash -c 'bash -x
    /abs/run.sh'``), or after a shell word bash reads as a command's name (``cat x | bash -c
    'a=1 while bash'``, where bash runs a command named while); in the command text, a -c
    string written with $'...' or $"..." quoting or holding an unquoted *, ?, [ or { (``bash
    -c $'echo hi'``), a process substitution given as the string, and a string built by
    expansion that names a listed interpreter, source or . (``bash -c "python3
    /abs/$f.py"``, ``bash -c "cd $d && ls ."``). Not refused by these tests: a name the
    string or body builds at run time (the deny-by-default rule refuses ``bash -c 'cat x |
    ${p}3 -'``, where the command so named receives a feed); an interpreter's name, an
    operator
    or a quote that an expansion supplies to a string built by expansion naming none of the
    listed names (``bash -c "$CMD"``, ``bash -c "b${E}ash"``), the residue of an eval; a
    name that brace expansion inside the string would build from parts that are not
    listed names (``bash -c 'py{thon3,} -'``); and a parse failure inside a -c string or an
    unquoted body whose text
    names no listed interpreter, source or . (``bash -c 'echo "a'``, ``cat <<EOF`` with an
    unterminated ``$(echo`` in the body), which bash itself rejects. A body whose delimiter
    has a quote or a backslash in it is never tested. The -c string is found by skipping
    the shell's options as bash reads them: --rcfile and --init-file take the next word; a
    cluster (-o, -ox, -xo, +o and the like) takes one word for each o or O in it, wherever
    the letter stands, in order (``bash -ox pipefail -c ...``, ``bash -oxo pipefail errexit
    -c ...``); -- and - end them, and a bare + is an empty option word that is skipped (bash, sh and
    dash read it so). For dash and sh, +s turns s off, so ``dash +s /abs/x.sh`` reads the script; the
    hook refuses it as it refuses bash +s (a stated over-refusal). An option that only an expansion supplies is not read as
    one. The inline
    programs of other interpreters (python -c, perl -e and the like) and of shells outside
    the list are not read.
  * a name built by a glob inside a -c string or an unquoted here-document body is not read
    as a listed name by the rules above (``bash -c 'cat /abs/run.sh | /bin/ba?h'``, ``bash
    -c 'cat /abs/run.sh | /usr/bin/pyth?n3 -'``, ``cat <<EOF`` with ``$(cat /abs/run.sh |
    /bin/ba?h)`` in the body); the deny-by-default rule refuses each of these. In an
    ordinary command such a name is refused only by that rule: one in a command with no
    standard-input shape and no argument that names standard input is not read
    (``/usr/bin/pyth?n3``, which python runs reading whatever standard input it inherits;
    ``/bin/ba?h < /abs/run.sh``, as ``bash < /abs/run.sh`` is allowed): allowed.
  * an env -S value inside a -c string is not read by the rules above (``bash -c 'env
    -Spython3'``, ``bash -c 'env --split-string=python3'``): allowed when the shell receives
    no feed; the deny-by-default rule refuses it when the shell receives one (``cat x |
    bash -c 'env -Spython3'``). In the command text itself both are refused.
  * a standard-input path spelt other than as listed above is not read as one by the rules
    above (``python3 //dev/stdin``, ``python3 /dev/./stdin``, ``python3
    /proc/thread-self/fd/0``, each with a here-string); the deny-by-default rule reads a
    path under /dev/fd/ or /proc/*/fd/ or naming /dev/std* as no program operand and
    refuses each of these.
  * a redirection of standard input whose descriptor is spelt other than 0 or nothing is
    not read as one (``bash 00<<<'echo hi'``, ``bash 00< <(cat /abs/run.sh)``): allowed
    by the rules above, refused by the deny-by-default rule.
  * an exec given only redirections, which sets the standard input of every later command
    in the shell, is not linked to those commands (``exec < <(cat /abs/run.sh); bash``):
    allowed by the rules above, refused by the deny-by-default rule.
  * sudo's own shell options are not read as running a shell (``cat /abs/run.sh | sudo
    -s``, ``cat /abs/run.sh | sudo -i``): allowed.
  * a quoted reserved word with no assignment before it is read as the command's name, as
    bash runs it (``cat /abs/run.sh | 'while' bash`` runs a command named while): allowed.
  * $"..." is read as its text untranslated: a message catalogue that would translate it
    is not read. In $'...', \\u and \\U above 0x7f are read as that Unicode character,
    whatever the locale's conversion would give.
  * anything this reader cannot see: a redirection applied to a whole group or loop rather
    than to a simple command, a case pattern inside $( ) or a case pattern spelt like a
    closing word, nested backticks, and any shell syntax it models differently from bash.

RESIDUAL. This hook is a best-effort text guard over an open shell grammar: it reads the
command text and never runs it, bash accepts forms that no reader of this size models, and
a line it allows is therefore not shown to keep an interpreter off standard input. The
forms below are known to be allowed and are not fixed; a test pins each one as allowed, so
that a change to any of them is seen:
  * a descriptor duplicated onto standard input is read as a named file (<& is a file
    feed), and a duplication written with >& onto descriptor 0 is not read as a feed at
    all, so a shell that reads a coproc's output is allowed (``coproc cat /abs/run.sh;
    bash <&63``, ``coproc cat /abs/run.sh; bash 0>&${COPROC[0]}``).
  * sudo's own shell options, which run a shell that reads the feed (``cat /abs/run.sh |
    sudo -s``, ``cat /abs/run.sh | sudo -i``).
  * a runner outside the modelled list, which runs its operands as a command unread
    (``cat /abs/run.sh | doas bash``).
  * an arithmetic command, which evaluates a variable's value again as an expression, so
    a subscript in that value may hold a substitution that runs (``x='a[$(bash)]'; cat
    /abs/run.sh | (( x ))``).
  * a variable whose one assignment never takes effect, resolved all the same: the level
    of the assignment is found by counting openers and closing words over the words before
    it, so a word spelt like a closing keyword (esac, fi, done, }) or a case pattern's )
    cancels an opener in the count, and an assignment inside an if, a group or a case arm
    that never runs is read as a top-level one, while bash leaves the variable unset and the
    interpreter reads its program from the feed (``echo esac; if false;
    then\\nT=/abs/s.py\\nfi; cat /abs/in.py | python3 -I $T``, each \\n a newline).
  * a function the line defines whose name is a modelled wrapper or a listed interpreter,
    which bash runs in place of the command of that name, and a function defined inside
    eval text: neither is read through its body (``nice() { bash; }; cat /abs/run.sh |
    nice grep y``).
  * a descriptor path spelt with a .. part, or spelt relative after a change of directory
    (cd /dev, then stdin), whose text, read after repeated slashes and . parts are dropped,
    keeps no dev/fd, dev/std or proc/NAME/fd part after that spelling (dev/fd and
    proc/NAME/fd each ending at a / or at the end of the text): such a path is read as a
    literal program operand though it names descriptor 0
    (``cat /abs/run.py | python3 /proc/self/task/../fd/0``). A spelling whose text keeps
    one of those parts is refused (``python3 /dev/fd/../fd/0``, ``python3 dev/stdin``
    after cd /).
  * a builtin that evaluates a quoted subscript as arithmetic (let, printf -v, [[ ]]
    arithmetic, declare -i, test -v), which runs a substitution in that subscript, and
    the substitution reads the feed (``cat /abs/run.sh | let 'a[$(bash)]'``).

Self-test: ``python3 -I .claude/hooks/block-stdin-interpreter.py --self-test``.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
import unicodedata

MAX_DEPTH = 24

STDIN_PATHS = frozenset(("/dev/stdin", "/dev/fd/0", "/proc/self/fd/0"))
STDIN_SHAPES = ("here-document", "here-string", "pipe", "process substitution")

_OPERATORS = tuple(sorted(("&>>", "<<<", "<<-", ";;&", "&&", "||", "|&", ";;", ";&", "<<",
                           ">>", "<&", ">&", "<>", ">|", "&>", "<", ">", "|", "&", ";", "(",
                           ")"), key=len, reverse=True))
REDIRECTIONS = frozenset(("&>>", "<<<", "<<-", "<<", ">>", "<&", ">&", "<>", ">|", "&>", "<",
                          ">"))
PIPES = frozenset(("|", "|&"))
KEYWORDS = frozenset(("!", "if", "then", "else", "elif", "do", "while", "until", "time",
                      "coproc"))
# Shell words after which bash reads the next word as a command's first word, so a NAME[
# there opens a subscript.
RESERVED = KEYWORDS | frozenset(("{", "}", "done", "fi", "esac"))
NOT_COMMANDS = frozenset(("for", "case", "select", "function", "in", "fi", "done", "esac",
                          "[[", "]]"))
# Reserved words bash reads as a command's name after an assignment (a=1 while bash runs a
# command named while). Skipped there, so the next word is the command (_argv), and refused
# in a command line that feeds standard input to an interpreter (_reserved_after_assignment).
# time is left to the time wrapper.
ASSIGNED_RESERVED = (KEYWORDS | NOT_COMMANDS | frozenset(("{", "}"))) - frozenset(("time",))
NAME_START = re.compile(r"[A-Za-z_]")
NAME_CHAR = re.compile(r"[A-Za-z0-9_]")
# A compound whose body shares its standard input, and the word that closes it.
COMPOUNDS = {"while": "done", "until": "done", "for": "done", "select": "done", "if": "fi",
             "case": "esac"}
CLOSERS = frozenset(("}", "done", "fi", "esac"))
# A word read as a function name before ( ): bash accepts more; any other word before ( ) is
# read as a command and a ( ) group.
FUNCTION_NAME = re.compile(r"[A-Za-z0-9_.:-]+")
# {NAME} or {NAME[...]} directly before < or >: bash reads it as the redirection's descriptor.
NAMED_DESCRIPTOR = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*(?:\[.*\])?\}", re.S)
# A command name's text that a glob or a brace expansion may change.
GLOB_SHAPE = re.compile(r"[*?]|\[.*\]|\{.*(?:,|\.\.).*\}", re.S)


class ParseError(Exception):
    """The command text cannot be read reliably; the hook refuses it (fail closed)."""


class Refused(Exception):
    """A presence test refused text this hook does not read; problem is (argv, reason)."""

    def __init__(self, argv, reason):
        super().__init__(reason)
        self.problem = (argv, reason)


class Uncertain(Exception):
    """Which word is a simple command's command cannot be determined with certainty.

    reason names why. always is True when the command is refused whatever its standard
    input is (wrappers nested past WRAPPER_LEVELS, a head or a word a wrapper reads
    built by a glob or a brace expansion, a sudo long option sudo's getopt_long would not
    read as one option); otherwise _decide_one refuses it only
    when it is fed standard input (_fed_standard_input).
    """

    def __init__(self, reason, always=False):
        super().__init__(reason)
        self.reason, self.always = reason, always


class Word:
    """One shell word: its text with quotes removed, and how it was written."""

    __slots__ = ("text", "quoted", "dynamic", "unread", "subs", "psubs", "literal", "head",
                 "brackets", "assign", "assign_end", "pattern", "arithmetic", "subscript")

    def __init__(self, text=""):
        self.text = ""
        self.quoted = False
        self.dynamic = False
        # $'...' or $"..." quoting, or an unquoted *, ?, [ or {: bash may pass text other
        # than self.text, so a -c string marked so is refused unread.
        self.unread = False
        self.pattern = False    # an unquoted *, ?, [ or { was written in the word
        # An unquoted NAME[ was read to its ] as a subscript (_lex_subscript): a pattern bash
        # expands when the word is not an assignment.
        self.subscript = False
        self.arithmetic = False     # an arithmetic command (( )), which runs no command
        self.subs = []          # token lists of $( ) and backtick substitutions in the word
        # (direction, tokens, keeps the command's standard input) of each <( ) or >( )
        # written inside the word: in a ${ } body or in an array assignment's list.
        self.psubs = []
        self.literal = True     # nothing but plain characters so far
        # How far the word so far reads as an assignment's left side: "name" (NAME), "sub"
        # (inside NAME[, with self.brackets open), "closed" (NAME[...]), "plus" (NAME+ or
        # NAME[...]+), or None when it cannot be one.
        self.head, self.brackets = "name", 0
        self.assign = False     # set at lex time: an unquoted NAME=, NAME+= or NAME[...]=
        self.assign_end = None  # begins the word; the length of text after that =
        self.add(text)

    def add(self, text, plain=True):
        """Append text; plain is False for text a quote, escape or expansion wrote.

        Only plain characters advance the assignment head; inside a subscript, quoted and
        expanded text is part of it, as bash reads it.
        """
        if not plain:
            self.literal = False
            if self.head != "sub":
                self.head = None
            self.text += text
            return
        for ch in text:
            self.text += ch
            self._step(ch)

    def _step(self, ch):
        head = self.head
        if head is None or self.assign:
            return
        if head == "sub":
            if ch == "[":
                self.brackets += 1
            elif ch == "]":
                self.brackets -= 1
                if not self.brackets:
                    self.head = "closed"
            return
        named = len(self.text) > 1
        if ch == "=" and named:
            self.assign, self.assign_end = True, len(self.text)
        elif head == "name" and (NAME_CHAR if named else NAME_START).fullmatch(ch):
            pass
        elif head == "name" and ch == "[" and named:
            self.head, self.brackets = "sub", 1
        elif ch == "+" and head in ("name", "closed") and named:
            self.head = "plus"
        else:
            self.head = None


def _text(item):
    if isinstance(item, Word):
        return item.text
    return item[1] + "(...)"


ARITH_UNSETTLED = ("a (( that bash may read either as arithmetic or as nested subshells (a "
                   "quote, backslash or backtick, or a comment or case in a substitution, "
                   "comes before its inner ( is closed)")


# Characters after which a # starts a word, so bash reads a comment from it.
COMMENT_BREAKS = frozenset(" \t\n;&|()<>")
# Words after which bash reads the next word as a command's first word, so a case there is
# the reserved word (-p and -- as time's).
CASE_LEADS = RESERVED | frozenset(("-p", "--"))
CASE_WORD = re.compile(r"case")


def _comment_or_case(text):
    """True when a command substitution's own text holds a comment or a case keyword as
    bash reads them: a # that starts a word (at the text's start, or after a blank, a
    newline or one of ; & | ( ) < >), or a case word in command position (at the text's
    start, after one of ; & | ( or a newline, or after a word such as do, then or {).
    A # inside a word (16#ff, $#, ${#x}) and case inside a word or as an argument
    (testcase, echo case) are neither."""
    for i, ch in enumerate(text):
        if ch == "#" and (i == 0 or text[i - 1] in COMMENT_BREAKS):
            return True
    for match in CASE_WORD.finditer(text):
        start, end = match.span()
        if start and text[start - 1] not in COMMENT_BREAKS:
            continue
        if end < len(text) and text[end] not in COMMENT_BREAKS:
            continue
        before = text[:start].rstrip(" \t")
        if not before or before[-1] in ";&|(\n":
            return True
        if re.split(r"[\s;&|()<>]", before)[-1] in CASE_LEADS:
            return True
    return False


def _arith_end(src, pos):
    """End of an arithmetic ((...)) whose (( is at pos, or None when bash reads nested ( ).

    bash reads (( as arithmetic only when the ) that matches the second ( is followed at
    once by ): it reads the body after (( as a matched pair and then checks the next
    character (``(( (1) ))`` and ``((1+(2)))`` are arithmetic; ``((true) && (bash))`` and
    ``(((:));(bash))`` are a subshell holding subshells, and their commands run). For $((
    bash keeps the arithmetic reading under the same condition (the body between $(( and
    the last )) must balance), else it runs a command substitution. The match is found by
    counting parentheses. bash's matched-pair reading skips a quoted or escaped parenthesis,
    and one in a comment or a case pattern inside a $( ); where such text comes before the
    match, the reading cannot be settled here and ParseError is raised (fail closed). The
    text of each $( ), between its ( and the ) the count matches to it, is what is read for
    a comment or case (_comment_or_case); the rest of the body is arithmetic, where a # is
    base notation (16#ff) and case may be part of a name.
    """
    depth, opened, unsettled = 0, [], False
    for i in range(pos + 2, len(src)):
        ch = src[i]
        if ch in "'\"`\\":
            raise ParseError(ARITH_UNSETTLED)
        if ch == "(":
            depth += 1
            if src[i - 1] == "$" and not src.startswith("(", i + 1):
                opened.append((depth, i + 1))
        elif ch == ")":
            if depth == 0:
                if unsettled:
                    raise ParseError(ARITH_UNSETTLED)
                return i + 2 if src.startswith(")", i + 1) else None
            if opened and opened[-1][0] == depth:
                unsettled = _comment_or_case(src[opened.pop()[1]:i]) or unsettled
            depth -= 1
    return None


def _brace_end(src, pos, in_double, depth, word):
    """End of a ${...} expansion whose body starts at pos.

    A $( ), backtick, ${ } or $(( )) in the body is read as it is anywhere else: the command
    text of each $( ) and backtick substitution goes to word.subs. An unquoted <( ) or >( )
    is read as a process substitution, as anywhere else, and goes to word.psubs.
    """
    if depth > MAX_DEPTH:
        raise ParseError("nesting deeper than " + str(MAX_DEPTH) + " levels")
    i, n = pos, len(src)
    while i < n:
        ch = src[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "'" and not in_double:
            end = src.find("'", i + 1)
            if end < 0:
                raise ParseError("an unterminated single quote inside ${ }")
            i = end + 1
            continue
        if ch == '"':
            inner = Word()
            i = _lex_double(src, i + 1, depth, inner)
            word.subs.extend(inner.subs)
            word.psubs.extend(inner.psubs)
            continue
        if ch == "$":
            inner = Word()
            i = _lex_dollar(src, i, depth, inner, in_double)
            word.subs.extend(inner.subs)
            word.psubs.extend(inner.psubs)
            continue
        if ch == "`":
            sub, i = _lex(src, i + 1, depth + 1, "`")
            word.subs.append(sub)
            continue
        if ch in "<>" and not in_double and src.startswith("(", i + 1):
            sub, i = _lex(src, i + 2, depth + 1, ")")
            word.psubs.append((ch, sub, False))
            continue
        if ch == "}":
            return i + 1
        i += 1
    raise ParseError("an unterminated ${ } expansion")


def _arith_subs(src, start, stop, depth, word):
    """Read the substitutions in the arithmetic body src[start:stop] into word.subs.

    $( ), backticks, ${ } and a nested $(( )) are read as anywhere else; a quote in the body
    is read as a plain character.
    """
    i = start
    while i < stop:
        ch = src[i]
        if ch == "\\":
            i = min(i + 2, stop)
        elif ch == "$":
            inner = Word()
            i = _lex_dollar(src, i, depth + 1, inner, True)
            word.subs.extend(inner.subs)
        elif ch == "`":
            sub, i = _lex(src, i + 1, depth + 1, "`")
            word.subs.append(sub)
        else:
            i += 1
    if i > stop:
        raise ParseError("a substitution that runs past the end of its arithmetic expression")


def _skip_body(src, pos, delimiter, strip_tabs):
    """Skip one here-document body: (where its terminator line starts, the position after
    that line); with no terminator the body runs to the end, as bash reads it."""
    n = len(src)
    while pos < n:
        end = src.find("\n", pos)
        line = src[pos:] if end < 0 else src[pos:end]
        if (line.lstrip("\t") if strip_tabs else line) == delimiter:
            return pos, (n if end < 0 else end + 1)
        if end < 0:
            return n, n
        pos = end + 1
    return n, n


# One-character escapes of $'...' quoting, as bash decodes them.
_ANSI_C_SIMPLE = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n",
                  "r": "\r", "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"', "?": "?"}
_HEX = frozenset("0123456789abcdefABCDEF")


def _ansi_c(body):
    r"""The text bash makes of a $'...' body: each escape decoded as bash decodes it.

    \nnn takes one to three octal digits, \xHH one or two hexadecimal digits, \uHHHH one
    to four and \UHHHHHHHH one to eight. \x{H...} is read as bash 5.3.9 reads it: every
    hexadecimal digit after the brace, the value's low byte kept, then one } when one
    follows (``$'\x{162}'`` is b; ``$'\x{6g2}'`` is 06 then g2}); with no digit the value
    is 0, a NUL. \cX is a control character made as bash makes it,
    from bytes and never from an uppercase form of X: the first byte of X's UTF-8
    encoding with its low five bits kept (0x7F for ?), then X's other bytes, each kept as
    the character of that byte value, as \xHH keeps a byte (``$'\c\u00df'`` is 03 9F);
    \c\\ takes both backslashes. A NUL ends the text, since bash keeps the decoded segment
    as a C string (``$'wh\0zz'ile`` is while).

    An escape bash does not decode (a character after the backslash with no escape
    meaning, \x, \u or \U with no digit after it, or \c at the end of the text) is kept as
    bash keeps it, a backslash followed by that character (``$'\q'`` is \q, ``$'\xg'`` is
    \xg). Fail closed: a \U value above 10FFFF, for which bash writes bytes this reader
    does not model, and any error while decoding raise ParseError, so the line is refused
    rather than read with a guess.
    """
    try:
        return _decode_ansi_c(body)
    except ParseError:
        raise
    except Exception as exc:
        raise ParseError("a $' ' quote whose escapes could not be decoded ("
                         + type(exc).__name__ + ")") from None


UNDECODED_ESCAPE = "a $' ' quote escape that this hook does not decode"


def _decode_ansi_c(body):
    """The decoding of _ansi_c, which turns any error raised here into a ParseError."""
    out, i, n = [], 0, len(body)
    while i < n:
        ch = body[i]
        if ch != "\\" or i + 1 >= n:
            out.append(ch)
            i += 1
            continue
        c, i = body[i + 1], i + 2
        if c in _ANSI_C_SIMPLE:
            out.append(_ANSI_C_SIMPLE[c])
        elif c in "01234567":
            j = i
            while j < n and j < i + 2 and body[j] in "01234567":
                j += 1
            out.append(chr(int(body[i - 1:j], 8) & 0xFF))
            i = j
        elif c == "x" and i < n and body[i] == "{":
            j = i + 1
            while j < n and body[j] in _HEX:
                j += 1
            out.append(chr(int(body[i + 1:j], 16) & 0xFF if j > i + 1 else 0))
            i = j + 1 if j < n and body[j] == "}" else j
        elif c in "xuU":
            j = i
            while j < n and j < i + {"x": 2, "u": 4, "U": 8}[c] and body[j] in _HEX:
                j += 1
            if j == i:
                out.append("\\" + c)        # bash keeps \x, \u or \U with no digit
                continue
            value = int(body[i:j], 16)
            if value > 0x10FFFF:
                raise ParseError(UNDECODED_ESCAPE + " (\\" + c + body[i:j] + ")")
            out.append(chr(value & 0xFF if c == "x" else value))
            i = j
        elif c == "c" and i < n:
            data = body[i].encode("utf-8")
            out.append(chr(0x7F if data[0] == 0x3F else data[0] & 0x1F))
            out.extend(chr(byte) for byte in data[1:])
            i += 1
            if body[i - 1] == "\\" and i < n and body[i] == "\\":
                i += 1              # bash reads \c\\ as a control backslash
        else:
            out.append("\\" + c)            # bash keeps an escape it does not decode
    return "".join(out).split("\0", 1)[0]


def _lex_dollar(src, pos, depth, word, in_double):
    """Read one $ form into word and return the position after it."""
    if src.startswith("$((", pos):
        end = _arith_end(src, pos + 1)
        if end is not None:
            _arith_subs(src, pos + 3, end - 2, depth, word)
            word.dynamic = True
            word.add(src[pos:end], plain=False)
            return end
    if src.startswith("$(", pos):
        sub, end = _lex(src, pos + 2, depth + 1, ")")
        word.subs.append(sub)
        word.dynamic = True
        word.add("$(...)", plain=False)
        return end
    if src.startswith("${", pos):
        end = _brace_end(src, pos + 2, in_double, depth + 1, word)
        word.dynamic = True
        word.add(src[pos:end], plain=False)
        return end
    if src.startswith("$[", pos):
        end = src.find("]", pos + 2)
        if end < 0:
            raise ParseError("an unterminated $[ ] expression")
        _arith_subs(src, pos + 2, end, depth, word)
        word.dynamic = True
        word.add(src[pos:end + 1], plain=False)
        return end + 1
    if not in_double and src.startswith("$'", pos):
        i = pos + 2
        while i < len(src) and src[i] != "'":
            i += 2 if src[i] == "\\" else 1
        if i >= len(src):
            raise ParseError("an unterminated $' ' quote")
        word.quoted = word.unread = True
        word.add(_ansi_c(src[pos + 2:i]), plain=False)
        return i + 1
    if not in_double and src.startswith('$"', pos):
        word.quoted = word.unread = True
        return _lex_double(src, pos + 2, depth, word)
    word.dynamic = True
    word.add("$", plain=False)
    return pos + 1


def _lex_double(src, pos, depth, word):
    """Read a double-quoted string body into word and return the position after the quote."""
    n = len(src)
    while pos < n:
        ch = src[pos]
        if ch == '"':
            return pos + 1
        if ch == "\\" and pos + 1 < n:
            nxt = src[pos + 1]
            if nxt == "\n":
                pos += 2
            elif nxt in '$`"\\':
                word.add(nxt, plain=False)
                pos += 2
            else:
                word.add(ch, plain=False)
                pos += 1
            continue
        if ch == "$":
            pos = _lex_dollar(src, pos, depth, word, True)
            continue
        if ch == "`":
            sub, pos = _lex(src, pos + 1, depth + 1, "`")
            word.subs.append(sub)
            word.dynamic = True
            word.add("`...`", plain=False)
            continue
        word.add(ch, plain=False)
        pos += 1
    raise ParseError("an unterminated double quote")


def _array_head(word):
    """True when word so far is an unquoted NAME=, NAME+= or NAME[i]=, so ( opens its list."""
    return word.assign and len(word.text) == word.assign_end


def _lex_subscript(src, pos, depth, word):
    """Read NAME's [ ... ] from pos (at the [) into word and return the position after its ].

    As bash reads it where an assignment may stand: the brackets nest, and blanks, operators,
    quotes and expansions inside are part of the word. Each $( ) and backtick in it goes to
    word.subs and is read with the standard input of the command the word is written in.
    """
    word.subscript = True
    word.add("[")
    i, n = pos + 1, len(src)
    while i < n:
        ch = src[i]
        if ch == "\\":
            word.add(src[i:i + 2], plain=False)
            i += 2
        elif ch == "'":
            end = src.find("'", i + 1)
            if end < 0:
                raise ParseError("an unterminated single quote inside a [ ] subscript")
            word.add(src[i + 1:end], plain=False)
            i = end + 1
        elif ch == '"':
            i = _lex_double(src, i + 1, depth, word)
        elif ch == "$":
            i = _lex_dollar(src, i, depth, word, False)
        elif ch == "`":
            sub, i = _lex(src, i + 1, depth + 1, "`")
            word.subs.append(sub)
            word.add("`...`", plain=False)
        else:
            word.add(ch)
            i += 1
            if word.head != "sub":
                return i
    raise ParseError("a NAME[ subscript with no matching ]")


def _next_place(place, word, target):
    """Where the word after word stands: "start" (a command's start, where shell words are
    read), "time" (after time there), "timeopt" (after time -p there), "redir" (after
    redirections written before any word), "assign" (after an assignment), or None
    (elsewhere, a reserved word after an assignment included, which bash reads as a
    command's name). bash skips a -- after time or time -p. An unquoted NAME[ opens a
    subscript in any of these places but None; target is True when word is a redirection's
    target."""
    if target:
        return "redir" if place in ("start", "time", "timeopt", "redir") else None
    bare = _bare(word)
    if place == "time" and bare == "-p":
        return "timeopt"
    if place in ("time", "timeopt") and bare == "--":
        return "start"
    if place in ("start", "time", "timeopt") and bare in RESERVED:
        return "time" if bare == "time" else "start"
    if place is not None and word.assign:
        return "assign"
    return None


def _lex_array(src, pos, depth, word):
    """Read the list of NAME=( ... ) from pos into word and return the position after its ).

    The elements are words, not commands. Each $( ), backtick and process substitution in
    them is kept in word.subs and word.psubs and is read with the standard input of the
    command the assignment is written in. Any operator but a newline in the list fails closed.
    """
    tokens, end = _lex(src, pos, depth, ")")
    for token in tokens:
        if token[0] == "W":
            word.subs.extend(token[1].subs)
            word.psubs.extend((ch, sub, True) for ch, sub, _keeps in token[1].psubs)
        elif token[0] == "PSUB":
            word.psubs.append((token[1], token[2], True))
        elif token[1] != "\n":
            raise ParseError("an operator inside an array assignment's list")
    word.dynamic = True
    word.add("(...)", plain=False)
    return end


def _lex(src, pos, depth, closer):
    """Tokens of src from pos up to closer (None, ')' or a backtick), and the end position.

    A token is ("W", Word), ("PSUB", "<" or ">", tokens) or ("OP", operator, fd).
    Here-document bodies are skipped, never tokenized.
    """
    if depth > MAX_DEPTH:
        raise ParseError("nesting deeper than " + str(MAX_DEPTH) + " levels")
    tokens, pending = [], []
    word, want_delimiter, paren = None, None, 0
    place, target = "start", False      # where the next word stands (_next_place)
    n = len(src)

    def flush():
        nonlocal word, want_delimiter, place, target
        if word is not None:
            if want_delimiter is not None:
                pending.append((word, want_delimiter))
                want_delimiter = None
            tokens.append(("W", word))
            place, target = _next_place(place, word, target), False
            word = None

    while pos < n:
        ch = src[pos]
        if ch == "`" and closer == "`":
            flush()
            if want_delimiter is not None or paren:
                raise ParseError("an unbalanced backtick substitution")
            return tokens, pos + 1
        if ch == "\\":
            if src.startswith("\\\n", pos):
                pos += 2
                continue
            word = word or Word()
            word.quoted = True
            word.add(src[pos + 1:pos + 2] or "\\", plain=False)
            pos += 2
            continue
        if ch == "'":
            end = src.find("'", pos + 1)
            if end < 0:
                raise ParseError("an unterminated single quote")
            word = word or Word()
            word.quoted = True
            word.add(src[pos + 1:end], plain=False)
            pos = end + 1
            continue
        if ch == '"':
            word = word or Word()
            word.quoted = True
            pos = _lex_double(src, pos + 1, depth, word)
            continue
        if ch == "$":
            word = word or Word()
            pos = _lex_dollar(src, pos, depth, word, False)
            continue
        if ch == "`":
            word = word or Word()
            sub, pos = _lex(src, pos + 1, depth + 1, "`")
            word.subs.append(sub)
            word.dynamic = True
            word.add("`...`", plain=False)
            continue
        if ch in " \t":
            flush()
            pos += 1
            continue
        if ch == "#" and word is None:
            end = src.find("\n", pos)
            pos = n if end < 0 else end
            continue
        if ch == "\n":
            flush()
            if want_delimiter is not None:
                raise ParseError("a here-document operator with no delimiter word")
            tokens.append(("OP", "\n", None))
            place, target = "start", False
            pos += 1
            for delimiter, strip_tabs in pending:
                body_end, after = _skip_body(src, pos, delimiter.text, strip_tabs)
                if not delimiter.quoted:
                    # An unquoted delimiter: bash expands the body. It is not parsed; the
                    # presence test refuses it unread.
                    body = src[pos:body_end]
                    if _body_presence(body, _plain_text(body)):
                        raise Refused([Word("<<" + delimiter.text)], BODY_REASON)
                pos = after
            pending.clear()
            continue
        if ch in "<>" and src.startswith("(", pos + 1):
            flush()
            sub, pos = _lex(src, pos + 2, depth + 1, ")")
            tokens.append(("PSUB", ch, sub))
            place = ("redir" if target and place in ("start", "time", "timeopt", "redir")
                     else None)
            target = False
            continue
        # (( at a command's start, also after a shell word such as do, while or { (place is
        # then still a command's start), is an arithmetic command, as bash reads it.
        if (src.startswith("((", pos) and word is None
                and (not tokens or (tokens[-1][0] == "OP" and tokens[-1][1] not in REDIRECTIONS)
                     or (tokens[-1][0] == "W" and place in ("start", "time", "timeopt")))):
            end = _arith_end(src, pos)
            if end is not None:
                arith = Word()
                _arith_subs(src, pos + 2, end - 2, depth, arith)
                arith.dynamic = True
                arith.arithmetic = True
                arith.add(src[pos:end], plain=False)
                tokens.append(("W", arith))
                place, target = None, False
                pos = end
                continue
        if ch == "(" and word is not None and _array_head(word):
            # NAME=( ... ), NAME+=( ... ), NAME[i]=( ... ): one assignment word whose elements
            # are words, never a word and a ( ) group.
            pos = _lex_array(src, pos + 1, depth + 1, word)
            continue
        op = next((o for o in _OPERATORS if src.startswith(o, pos)), None)
        if op is None:
            word = word or Word()
            if ch == "[" and word.head == "name" and word.text and place and not target:
                # NAME[ where an assignment may stand: bash reads to the matching ].
                pos = _lex_subscript(src, pos, depth, word)
                continue
            if ch in "*?[{":
                word.unread = True      # a pattern or a brace expansion bash may expand
                word.pattern = True
            word.add(ch)
            pos += 1
            continue
        fd = None
        if op in REDIRECTIONS and word is not None and word.literal and word.text.isdigit():
            fd, word = word.text, None
        elif (op in REDIRECTIONS and op[0] in "<>" and word is not None
              and NAMED_DESCRIPTOR.fullmatch(word.text)):
            # bash opens a new descriptor and stores its number in NAME, so the word is not
            # a command word. The Word itself is kept as the descriptor, so a substitution
            # in its subscript is still read.
            fd, word = word, None
        flush()
        if want_delimiter is not None:
            raise ParseError("a here-document operator with no delimiter word")
        pos += len(op)
        if op == "(":
            paren += 1
        elif op == ")":
            if paren:
                paren -= 1
            elif closer == ")":
                return tokens, pos
            # Otherwise an unmatched ) ends a case pattern: it separates like ;.
        tokens.append(("OP", op, fd))
        if op in REDIRECTIONS:
            target = True
        else:
            place, target = (None if op in (";;", ";&", ";;&") else "start"), False
        if op in ("<<", "<<-"):
            want_delimiter = op == "<<-"
    flush()
    if want_delimiter is not None:
        raise ParseError("a here-document operator with no delimiter word")
    if closer == ")":
        raise ParseError("an unterminated $( ) or <( ) substitution")
    if closer == "`":
        raise ParseError("an unterminated backtick substitution")
    if paren:
        raise ParseError("an unclosed ( group")
    return tokens, pos


class Simple:
    """One simple command: its words, and the shape of its standard input."""

    def __init__(self, piped):
        self.items, self.stdin, self.piped = [], None, piped

    def shape(self):
        # piped is True for a pipe, or the shape's name a -c string's shell was given.
        if self.stdin:
            return self.stdin
        if isinstance(self.piped, str):
            return self.piped
        return "pipe" if self.piped else None


def _bare(item):
    """The text of an unquoted word with no expansion in it, else None."""
    if isinstance(item, Word) and not item.quoted and not item.dynamic:
        return item.text
    return None


def _coproc_name(cur):
    """True when cur ends in ``coproc NAME``, the head of a named coproc."""
    items = cur.items
    return (len(items) >= 2 and _bare(items[-2]) == "coproc" and _bare(items[-1]) is not None
            and items[-1].text not in KEYWORDS and items[-1].text not in NOT_COMMANDS)


def _at_start(cur):
    """True when cur holds nothing but shell words, so a group or compound may open here.

    A coproc's NAME counts with the shell words: ``coproc NAME`` opens the compound command
    after it as ``coproc`` alone does.
    """
    items = cur.items[:-1] if _coproc_name(cur) else cur.items
    return all(_bare(item) in KEYWORDS for item in items)


def _open_here(cur, out):
    """Finish cur where a group or compound opens; a coproc's NAME names it and runs nothing."""
    if _coproc_name(cur) and _at_start(cur):
        cur.items.pop()
    if cur.items:
        out.append(cur)


def _after_keywords(cur):
    """cur's items after its leading shell words (not coproc, whose next word may be a name)."""
    j = 0
    while (j < len(cur.items) and _bare(cur.items[j]) in KEYWORDS
           and cur.items[j].text != "coproc"):
        j += 1
    return cur.items[j:]


def _function_keyword(cur):
    """True when cur is ``function NAME`` after any shell words, a function definition's head."""
    items = _after_keywords(cur)
    return len(items) == 2 and _bare(items[0]) == "function" and _bare(items[1]) is not None


def _function_name(cur):
    """True when cur is one word after any shell words that a following ``( )`` makes a
    function name: a word FUNCTION_NAME accepts. An assignment never qualifies, since
    FUNCTION_NAME has no =, and ``a=()`` is lexed as one assignment word in any case."""
    items = _after_keywords(cur)
    name = _bare(items[0]) if len(items) == 1 else None
    return (name is not None and name not in KEYWORDS and name not in NOT_COMMANDS
            and FUNCTION_NAME.fullmatch(name) is not None)


def _read_psubs(word, piped, out):
    """Append the commands of each process substitution inside word to out.

    A >( ) reads through a pipe, as anywhere else; a <( ) reads alone, except in an array
    assignment's list, where it keeps piped, the standard input of the command.
    """
    for ch, sub, keeps in word.psubs:
        _commands(sub, out, ch == ">" or (keeps and piped))


def _commands(tokens, out, base=False):
    """Append every simple command in tokens to out, substitutions included.

    base is True when standard input is a pipe: a $( ) or backtick substitution runs with
    the standard input of the command it is written in.
    """
    # Per open group or compound: [closing word, stdin is a pipe, a for or select head that
    # has not yet reached its do or { body].
    groups = []
    cur = Simple(base)
    after_pipe = False              # | or |& just read: a newline (or comment) continues it
    fdef = False                    # NAME ( ) just read: a newline before the body goes on
    i = 0
    while i < len(tokens):
        kind = tokens[i][0]
        if kind == "W":
            after_pipe = fdef = False
            word = tokens[i][1]
            for sub in word.subs:
                _commands(sub, out, cur.piped)
            _read_psubs(word, cur.piped, out)
            bare = _bare(word)
            keyword_head = _function_keyword(cur)
            if bare == "{" and (_at_start(cur) or keyword_head):
                _open_here(cur, out)
                if keyword_head:
                    piped = False   # a function body runs when called, not under this pipe
                elif groups and groups[-1][2]:
                    piped = groups.pop()[1]     # for or select NAME ...; { }: the body
                else:
                    piped = cur.piped
                groups.append(["}", piped, False])
                cur = Simple(piped)
            elif bare in COMPOUNDS and _at_start(cur):
                _open_here(cur, out)
                groups.append([COMPOUNDS[bare], cur.piped, bare in ("for", "select")])
                cur = Simple(cur.piped)
                cur.items.append(word)
            elif bare in CLOSERS and not cur.items and (bare == "}" or (
                    groups and groups[-1][0] == bare)):
                if groups and groups[-1][0] == bare:
                    groups.pop()
                cur = Simple(groups[-1][1] if groups else base)
            else:
                if bare == "do" and groups and groups[-1][2] and (_at_start(cur) or (
                        len(cur.items) == 2 and _bare(cur.items[0]) in ("for", "select"))):
                    # The for or select head ends at do: at a command start after its in
                    # list, or right after NAME when it has none (for NAME do).
                    groups[-1][2] = False
                    if cur.items:
                        out.append(cur)
                    cur = Simple(groups[-1][1])
                cur.items.append(word)
        elif kind == "PSUB":
            after_pipe = fdef = False
            # >( ) reads, through a pipe, what this command writes to it; <( ) reads alone.
            _commands(tokens[i][2], out, tokens[i][1] == ">")
            cur.items.append(tokens[i])
        else:
            op, fd = tokens[i][1], tokens[i][2]
            if op in REDIRECTIONS:
                target = tokens[i + 1] if i + 1 < len(tokens) else None
                if target is None or target[0] == "OP":
                    raise ParseError("a redirection with no target")
                psub = target[0] == "PSUB" or bool(target[1].psubs)
                if target[0] == "W":
                    for sub in target[1].subs:
                        _commands(sub, out, cur.piped)
                    _read_psubs(target[1], cur.piped, out)
                else:
                    _commands(target[2], out, target[1] == ">")
                if isinstance(fd, Word):
                    for sub in fd.subs:
                        _commands(sub, out, cur.piped)
                    _read_psubs(fd, cur.piped, out)
                if fd in (None, "0"):
                    if op in ("<<", "<<-"):
                        cur.stdin = "here-document"
                    elif op == "<<<":
                        cur.stdin = "here-string"
                    elif op == "<":
                        cur.stdin = "process substitution" if psub else "file"
                after_pipe = False
                i += 2
                continue
            if op == "\n" and (after_pipe or fdef or _function_keyword(cur)):
                i += 1                  # the pipeline or function definition goes on
                continue
            if (op == "(" and i + 1 < len(tokens) and tokens[i + 1][:2] == ("OP", ")")
                    and (_function_keyword(cur) or _function_name(cur))):
                # NAME ( ) or function NAME ( ): a definition, not a command, and its body
                # is not under the pipe.
                after_pipe, fdef = False, True
                cur = Simple(False)
                i += 2
                continue
            fdef = False
            opens_piped = cur.piped and _at_start(cur)
            if op == "(":
                _open_here(cur, out)
            elif cur.items:
                out.append(cur)
            after_pipe = op in PIPES
            if op in PIPES:
                cur = Simple(True)
            elif op == "(":
                groups.append([")", opens_piped, False])
                cur = Simple(groups[-1][1])
            else:
                # A ) closes a ( ) group only when that group is the innermost open entry;
                # inside case ... esac it ends a pattern.
                if op == ")" and groups and groups[-1][0] == ")":
                    groups.pop()
                cur = Simple(groups[-1][1] if groups else base)
        i += 1
    if cur.items:
        out.append(cur)


def _plain(text):
    return Word(text)


def _skip_options(args, takes_argument=()):
    j = 0
    while j < len(args):
        t = _text(args[j])
        if t == "--":
            return args[j + 1:]
        if t in takes_argument:
            j += 2
        elif t.startswith("-") and t != "-":
            j += 1
        else:
            break
    return args[j:]


def _skip_cluster(args, arg_chars):
    """args after a wrapper's options, its one-letter options possibly clustered.

    As for env, the first letter of a cluster found in arg_chars takes the rest of the word
    as its argument, or else the next word (-Eu NAME, -ca NAME, -uNAME).
    """
    j = 0
    while j < len(args):
        t = _text(args[j])
        if t == "--":
            return args[j + 1:]
        if t.startswith("--"):
            j += 1
        elif len(t) > 1 and t[0] == "-":
            k = next((k for k in range(1, len(t)) if t[k] in arg_chars), None)
            j += 2 if k == len(t) - 1 else 1
        else:
            break
    return args[j:]


def _sets_a_variable(item):
    """True when item is a NAME=VALUE operand of env or sudo: a word holding an =.

    GNU env reads every operand that holds an = after its options as an environment entry,
    whatever the text before the = (\\q=1, a-b=1, 1=1 and =1 included), and runs the
    first operand without one as the command; sudo is read the same way for its VAR=value
    operands. bash's rule for a valid identifier does not apply to these operands.
    """
    return isinstance(item, Word) and "=" in item.text


def _skip_assignments(args):
    """args after the leading NAME=VALUE operands of env or sudo (_sets_a_variable)."""
    j = 0
    while j < len(args) and _sets_a_variable(args[j]):
        j += 1
    return args[j:]


def _env_split(payload, rest, strict=False):
    # GNU env -S reads backslash escapes (\_ among them, a separator), ${NAME} references
    # and a # comment, and splits on a vertical tab and a form feed; shlex reads none of
    # them as GNU env does, so in strict mode such text is refused, not split.
    if strict and any(ch in payload for ch in ENV_SPLIT_CHARACTERS):
        raise Uncertain(ENV_SPLIT_REASON)
    try:
        split = shlex.split(payload)
    except ValueError:
        raise ParseError("an env -S string that cannot be split") from None
    return _after_env([_plain(s) for s in split] + list(rest), strict)


def _after_env(args, strict=False):
    j = 0
    while j < len(args):
        t = _text(args[j])
        if t in ("-u", "--unset", "-C", "--chdir"):
            j += 2
            continue
        if t in ("-S", "--split-string") or t.startswith(("--split-string=", "-S")):
            if t in ("-S", "--split-string"):
                if j + 1 >= len(args):
                    return []
                payload, j = _text(args[j + 1]), j + 2
            else:
                payload, j = (t.split("=", 1)[1] if t.startswith("--") else t[2:]), j + 1
            return _env_split(payload, args[j:], strict)
        if t == "--":
            j += 1
            break
        if len(t) > 1 and t[0] == "-" and t[1] != "-":
            # A cluster (-iC DIR, -iu NAME, -iS 'cmd'): the first u, C or S takes the rest of
            # the word as its argument, or the next word when nothing follows it.
            k = next((k for k in range(1, len(t)) if t[k] in "uCS"), None)
            if k is None:
                j += 1
                continue
            if t[k + 1:]:
                value, j = t[k + 1:], j + 1
            elif j + 1 < len(args):
                value, j = _text(args[j + 1]), j + 2
            else:
                return []
            if t[k] == "S":
                return _env_split(value, args[j:], strict)
            continue
        if t.startswith("-"):
            j += 1
            continue
        if _sets_a_variable(args[j]):
            j += 1
            continue
        break
    return _skip_assignments(args[j:])


def _after_nice(args):
    j = 0
    while j < len(args):
        t = _text(args[j])
        if t in ("-n", "--adjustment"):
            j += 2
        elif t == "--":
            return args[j + 1:]
        elif t.startswith("-") and t != "-":
            j += 1
        else:
            break
    return args[j:]


def _after_timeout(args):
    rest = _skip_options(args, ("-s", "--signal", "-k", "--kill-after"))
    return rest[1:]                 # the duration


# sudo's full option table, from its manual, sudo(8), upstream at
# https://www.sudo.ws/docs/man/sudo.man/ (the latest version, read 2026-11-17): True when
# the option takes an argument. The manual lists 13 options with a required argument: -a,
# -C, -c, -D, -g, -h host, -p, -R, -r, -T, -t, -U and -u, with their long forms
# --auth-type, --close-from, --login-class, --chdir, --group, --host, --prompt, --chroot,
# --role, --command-timeout, --type, --other-user and --user. It lists --preserve-env=list
# with a required list, read here only after an =, and -E (--preserve-env) with none, so
# --preserve-env as a word of its own is read as taking none. It also lists -h with no
# argument as --help, so -h with nothing attached may take the next word or not: it is in
# SUDO_SHORT_EITHER_KIND and refused when the command is fed standard input. -hHOST and
# --host=HOST carry their argument, and --help takes none.
SUDO_SHORT_OPTIONS = {
    "A": False, "a": True, "B": False, "b": False, "C": True, "c": True, "D": True,
    "E": False, "e": False, "g": True, "H": False, "h": True, "i": False, "K": False,
    "k": False, "l": False, "N": False, "n": False, "P": False, "p": True, "R": True,
    "r": True, "S": False, "s": False, "T": True, "t": True, "U": True, "u": True,
    "V": False, "v": False,
}
SUDO_LONG_OPTIONS = {
    "askpass": False, "auth-type": True, "background": False, "bell": False,
    "close-from": True, "login-class": True, "chdir": True, "preserve-env": False,
    "edit": False, "group": True, "set-home": False, "help": False, "host": True,
    "login": False, "remove-timestamp": False, "reset-timestamp": False, "list": False,
    "no-update": False, "non-interactive": False, "preserve-groups": False,
    "prompt": True, "chroot": True, "role": True, "stdin": False, "shell": False,
    "command-timeout": True, "type": True, "other-user": True, "user": True,
    "version": False, "validate": False,
}
# Long options that take a value only after an =, never as the next word.
SUDO_LONG_EQUALS_ONLY = frozenset(("preserve-env",))
# Short options the manual lists both with no argument and with one (-h as --help and as
# -h host): with nothing attached, whether the next word is the argument is not known.
SUDO_SHORT_EITHER_KIND = frozenset(("h",))


def _sudo_long_option(given):
    """The sudo long option given names, as sudo's getopt_long reads it, or None.

    An exact long name is that option; otherwise a prefix of exactly one long name is that
    option and takes its argument kind (--us is --user). A prefix of more than one long name
    (--log: --login and --login-class) and a name no long name starts with give None: sudo
    rejects them, and a later sudo may add a long name that makes them its own, so whether
    they take the next word is not known.
    """
    if given in SUDO_LONG_OPTIONS:
        return given
    names = [name for name in SUDO_LONG_OPTIONS if name.startswith(given)]
    return names[0] if len(names) == 1 else None


def _after_sudo(args, strict=False):
    """args after sudo's options, each read from sudo's full option table.

    A short option that takes an argument takes the rest of the word, or else the next
    word, also at the end of a cluster (-Eu NAME, -uNAME); a long one takes the text after
    an = or else the next word (--user=NAME, --user NAME). A long option is looked up with
    its =value stripped, as sudo's getopt_long looks it up (_sudo_long_option): an exact
    long name, or else a prefix of exactly one long name (--us NAME is --user NAME). -- ends
    the options and the first word that is not option-shaped is the command. A long option
    that names no one option that way (not in the table, or a prefix of more than one long
    name) raises Uncertain in either mode, refused whatever the standard input is, since
    whether it takes the next word decides which word is the command. In strict mode (a
    command fed standard input) Uncertain is also raised for an option-shaped word that
    is not literal text, a short option not in the table, and a long option that takes no
    argument given one after an =: the = means it takes no next word, but the table says
    it takes no value, so the line is not one the table describes. Outside strict mode
    such a short option is read as taking no argument, and such a long option as taking
    no next word. -h with nothing attached (-h, -Eh) raises Uncertain in strict mode too,
    since the manual lists it both as --help and as -h host; outside strict mode it is
    read as taking the next word. -hHOST and --host=HOST carry their argument.
    """
    j = 0
    while j < len(args):
        t = _text(args[j])
        if t == "--":
            return args[j + 1:]
        if len(t) < 2 or t[0] != "-":
            break
        if strict and _not_literal(args[j]):
            raise Uncertain(OPERAND_REASON)
        step = 1
        if t.startswith("--"):
            given, equals, _value = t[2:].partition("=")
            name = _sudo_long_option(given)
            if name is None:
                raise Uncertain(SUDO_LONG_OPTION_REASON, always=True)
            takes = SUDO_LONG_OPTIONS[name]
            if equals and not takes and name not in SUDO_LONG_EQUALS_ONLY:
                if strict:
                    raise Uncertain(SUDO_VALUE_REASON)
            elif takes and not equals:
                step = 2
        else:
            for k in range(1, len(t)):
                takes = SUDO_SHORT_OPTIONS.get(t[k])
                if takes is None:
                    if strict:
                        raise Uncertain(SUDO_OPTION_REASON)
                    continue
                if takes:
                    if k == len(t) - 1:
                        if strict and t[k] in SUDO_SHORT_EITHER_KIND:
                            raise Uncertain(SUDO_EITHER_KIND_REASON)
                        step = 2
                    break
        j += step
    return args[j:]


WRAPPERS = frozenset(("env", "command", "exec", "nice", "timeout", "nohup", "sudo", "time"))
WRAPPER_LEVELS = 16
UNCERTAIN_REASON = ("which word is the command cannot be determined with certainty ({}), "
                    "while the command is fed standard input or given -, a standard-input "
                    "path or a process substitution, so it is refused rather than guessed")
COMMAND_WORD_REASON = ("the word in command position is not literal text but an expansion or "
                       "a substitution")
OPERAND_REASON = ("a word a wrapper reads as its option, option argument or operand is not "
                  "literal text but an expansion, a substitution or a glob")
ENV_SPLIT_CHARACTERS = ("\\", "$", "#", "\v", "\f")
ENV_SPLIT_REASON = ("the env -S text holds a backslash, a $, a # or a vertical tab or form "
                    "feed: GNU env reads a backslash as an escape, a $ as a variable "
                    "reference and a # as a comment, and splits on a vertical tab or form "
                    "feed outside quotes, which this hook does not do as GNU env does")
SUDO_ORDER_REASON = ("a sudo NAME=VALUE operand is followed by an option-shaped operand, which "
                     "sudo may read as an option")
SUDO_OPTION_REASON = ("a sudo short option is not in sudo's option table, so whether it "
                      "takes the next word is not known")
SUDO_VALUE_REASON = ("a sudo long option that takes no argument is given one after an =: the "
                     "= means it takes no next word, but sudo's option table says it takes "
                     "no value, so the line is not one the table describes")
ALWAYS_UNCERTAIN_REASON = ("which word is the command cannot be determined with certainty "
                           "({}), so it is refused rather than guessed, whatever the "
                           "standard input is")
SUDO_LONG_OPTION_REASON = ALWAYS_UNCERTAIN_REASON.format(
    "a sudo long option is neither one of sudo's long names nor a prefix of exactly one of "
    "them, as sudo's getopt_long reads an abbreviation, so whether it takes the next word "
    "is not known")
WRAPPER_PATTERN_REASON = ALWAYS_UNCERTAIN_REASON.format(
    "the command name is built by a glob or a brace expansion, which this hook does not "
    "expand, and it may name a wrapper, so which command runs and how the words after it "
    "are read are not known")
WRAPPER_OPERAND_PATTERN_REASON = ALWAYS_UNCERTAIN_REASON.format(
    "a word a wrapper reads as its option, option argument or operand is built by a glob "
    "or a brace expansion, which this hook does not expand, so which word is the command "
    "is not known")
SUDO_EITHER_KIND_REASON = ("a sudo -h has nothing attached, and sudo's manual lists -h both "
                           "as its help option, which takes no argument, and as its host "
                           "option, which takes one, so whether it takes the next word is "
                           "not known")
DEPTH_REASON = ("more than " + str(WRAPPER_LEVELS) + " wrappers are nested, so the command "
                "after them is not read; this is refused whatever the standard input is")


def _not_literal(item):
    """True when item is not literal text: a process substitution, or a word holding an
    expansion, a substitution or a glob or brace expansion."""
    return (not isinstance(item, Word) or item.dynamic or bool(item.psubs)
            or _built_by_expansion(item))


def _unwrap(argv, strict=False):
    """argv with leading wrappers and their options removed ([] when nothing is run).

    In strict mode (a command fed standard input) Uncertain is raised where the command
    word cannot be determined with certainty: a command word that is not literal text, a
    word a wrapper reads that is not literal text, env -S text this hook does not split as
    GNU env does, a sudo option outside sudo's option table (_after_sudo), and a sudo
    NAME=VALUE operand followed by an option-shaped operand.
    Wrappers nested more than WRAPPER_LEVELS deep raise Uncertain in either mode, and so do
    a head built by a glob or a brace expansion, a word a wrapper reads as its option,
    option argument or operand so built, and a sudo long option sudo's getopt_long would
    not read as one option (_after_sudo): which command runs, and so whether a nested -c
    program is read, is not known. What such a pattern matches is not worked out.
    """
    levels = 0
    while argv:
        head = argv[0]
        if not isinstance(head, Word) or head.dynamic or head.psubs:
            if strict:
                raise Uncertain(COMMAND_WORD_REASON)
            return argv
        if _built_by_expansion(head):
            # A name written as a pattern (/b*/env, e[[:alpha:]]v, /b{in,in}/env) is not
            # expanded here, and what it matches is not worked out: a bracket expression
            # may hold a character class, an equivalence class or a collating symbol, and a
            # brace expansion may give any number of words. Any such name may name a
            # wrapper, and the words after it may be a shell given a -c program that is
            # never read, so it is refused in any line, fed or not.
            raise Uncertain(WRAPPER_PATTERN_REASON, always=True)
        name = os.path.basename(head.text)
        if name not in WRAPPERS:
            return argv
        if levels == WRAPPER_LEVELS:
            raise Uncertain(DEPTH_REASON, always=True)
        levels += 1
        rest = list(argv[1:])
        if name == "env":
            argv = _after_env(rest, strict)
        elif name == "command":
            j = 0
            while j < len(rest) and _text(rest[j]).startswith("-") and _text(rest[j]) != "-":
                if isinstance(rest[j], Word) and _built_by_expansion(rest[j]):
                    raise Uncertain(WRAPPER_OPERAND_PATTERN_REASON, always=True)
                t = _text(rest[j])
                j += 1
                if t == "--":
                    break
                if "v" in t or "V" in t:
                    return []       # command -v and -V only look the name up
            argv = rest[j:]
        elif name == "exec":
            argv = _skip_cluster(rest, "a")
        elif name == "nice":
            argv = _after_nice(rest)
        elif name == "timeout":
            argv = _after_timeout(rest)
        elif name == "nohup":
            argv = _skip_options(rest)
        elif name == "sudo":
            options = _after_sudo(rest, strict)
            argv = _skip_assignments(options)
            if (strict and len(argv) < len(options) and argv
                    and _text(argv[0]).startswith("-")):
                raise Uncertain(SUDO_ORDER_REASON)
        else:
            argv = _skip_options(rest, ("-f", "-o", "--format", "--output"))
        # A word the wrapper read as its option, option argument or operand that a glob
        # or a brace expansion may turn into other words, or into several, changes which
        # word is the command: refused in any line, fed or not.
        kept = {id(item) for item in argv}
        if any(isinstance(item, Word) and _built_by_expansion(item)
               for item in rest if id(item) not in kept):
            raise Uncertain(WRAPPER_OPERAND_PATTERN_REASON, always=True)
        if strict and any(_not_literal(item) for item in rest if id(item) not in kept):
            raise Uncertain(OPERAND_REASON)
    return argv


def _argv(items, strict=False):
    """The effective argv of a simple command: assignments, shell words and wrappers skipped.

    A shell word is read as one only before the first assignment: bash reads it as a shell
    word only at a command's start, so ``a=1 while bash`` runs a command named while. That
    form is read fail closed: after an assignment a reserved word, quoted or not, is
    skipped (ASSIGNED_RESERVED), so an interpreter after it is checked as the command;
    _reserved_after_assignment refuses the form in a line that feeds an interpreter.
    strict is passed to _unwrap. An arithmetic command (( )) standing alone after any shell
    words runs no command, so [] is returned for it.
    """
    i, assigned = 0, False
    while i < len(items):
        item = items[i]
        if not isinstance(item, Word):
            break
        if item.arithmetic and i == len(items) - 1:
            # An arithmetic command (( )) runs no command: bash evaluates it in the shell.
            # A substitution inside it is read by _commands, as in any word. With a word
            # after it in the same simple command, which bash rejects, it is read as
            # before, as an expansion in command position.
            return []
        if item.assign:
            i, assigned = i + 1, True
            continue
        if assigned:
            if not item.dynamic and item.text in ASSIGNED_RESERVED:
                i += 1
                continue
            break
        bare = None if item.quoted or item.dynamic else item.text
        if bare in KEYWORDS:
            i += 1
            if bare == "time":
                # bash skips -p, --, or -p then --, after the time shell word.
                if i < len(items) and _text(items[i]) == "-p":
                    i += 1
                if i < len(items) and _text(items[i]) == "--":
                    i += 1
            continue
        if bare in NOT_COMMANDS:
            return []
        break
    return _unwrap(items[i:], strict)


class Spec:
    """How one interpreter family spells its options."""

    def __init__(self, *, shell=False, cluster=True, inline_chars="", module_chars="",
                 info_chars="", arg_chars="", attached_chars="", digit_chars="",
                 stdin_char="", inline=(), inline_prefixes=(), script=(), long_args=(),
                 info=()):
        self.shell, self.cluster = shell, cluster
        self.inline_chars, self.module_chars = inline_chars, module_chars
        self.info_chars, self.arg_chars = info_chars, arg_chars
        self.attached_chars, self.digit_chars = attached_chars, digit_chars
        self.stdin_char = stdin_char
        self.inline, self.inline_prefixes = frozenset(inline), tuple(inline_prefixes)
        self.script, self.long_args, self.info = frozenset(script), frozenset(long_args), frozenset(info)


PYTHON = Spec(inline_chars="c", module_chars="m", info_chars="Vh?", arg_chars="WX",
              long_args=("--check-hash-based-pycs",),
              info=("--version", "--help", "--help-env", "--help-xoptions", "--help-all"))
PERL = Spec(inline_chars="eE", info_chars="vVh", arg_chars="I", attached_chars="MmiCdDxF",
            digit_chars="l0", info=("--version", "--help"))
RUBY = Spec(inline_chars="e", info_chars="vh", arg_chars="IrCE", attached_chars="0iTWxKF",
            long_args=("--enable", "--disable", "--encoding", "--external-encoding",
                       "--internal-encoding"),
            info=("--version", "--help", "--copyright"))
NODE = Spec(cluster=False, inline=("-e", "--eval", "-p", "--print", "-pe", "-ep"),
            inline_prefixes=("--eval=", "--print="),
            long_args=("-r", "--require", "--import", "--loader", "--experimental-loader",
                       "--input-type", "--title", "-C", "--conditions", "--env-file"),
            info=("-v", "--version", "-h", "--help", "--v8-options"))
PHP = Spec(cluster=False, inline=("-r", "-R", "-B", "-E"), script=("-f", "-F"),
           long_args=("-c", "-d", "-z", "-t"),
           info=("-v", "-h", "-i", "-m", "-?", "-S", "--version", "--help", "--info",
                 "--modules", "--ini", "--rf", "--rc", "--re", "--rz", "--ri"))
SHELL = Spec(shell=True, inline_chars="c", stdin_char="s", arg_chars="oO",
             long_args=("--rcfile", "--init-file"), info=("--version", "--help"))

_FAMILIES = (
    (re.compile(r"python(?:\d+(?:\.\d+)*t?)?"), PYTHON),
    (re.compile(r"perl(?:\d+(?:\.\d+)*)?"), PERL),
    (re.compile(r"ruby(?:\d+(?:\.\d+)*)?"), RUBY),
    (re.compile(r"php(?:\d+(?:\.\d+)*)?"), PHP),
    (re.compile(r"node(?:js)?"), NODE),
    (re.compile(r"r?bash|sh|zsh|dash"), SHELL),
)


def _spec_for(name):
    for pattern, spec in _FAMILIES:
        if pattern.fullmatch(name):
            return spec
    return None


def _shell_option_arguments(word):
    """How many following words a shell option cluster (-ox, -oxo, +o) takes.

    bash reads each o or O in a cluster, wherever it stands, as taking the next unused
    word, in order: ``bash -oxo pipefail errexit`` takes both words.
    """
    return sum(ch in SHELL.arg_chars for ch in word[1:])


def _scan(args, spec):
    """(mode, operand): mode is inline, module, info, stdin, stdin-flag or operand."""
    stdin_flag = False
    j = 0
    while j < len(args):
        item = args[j]
        if not isinstance(item, Word):
            break
        t = item.text
        if t == "--":
            j += 1
            break
        if t == "-":
            if spec.shell:
                j += 1
                break
            return "stdin", item
        if t in spec.info:
            return "info", None
        if t in spec.inline or (spec.inline_prefixes and t.startswith(spec.inline_prefixes)):
            return "inline", None
        if t in spec.script:
            return "operand", (args[j + 1] if j + 1 < len(args) else None)
        if t in spec.long_args:
            j += 2
            continue
        if t.startswith("--"):
            j += 1
            continue
        if spec.shell and t == "+":
            # bash, sh and dash read a bare + as an empty option word.
            j += 1
            continue
        if spec.shell and len(t) > 1 and t[0] in "-+":
            # bash reads c and s in a + cluster as in a - cluster
            # (bash +c, +xc, +oc pipefail, +s), so both tests apply to either sign.
            if any(ch in spec.inline_chars for ch in t[1:]):
                return "inline", None
            stdin_flag = stdin_flag or spec.stdin_char in t[1:]
            j += 1 + _shell_option_arguments(t)
            continue
        if len(t) > 1 and t[0] == "-":
            if not spec.cluster:
                j += 1
                continue
            k, take_next = 1, False
            while k < len(t):
                ch = t[k]
                if ch in spec.inline_chars:
                    return "inline", None
                if ch in spec.module_chars:
                    return "module", None
                if ch in spec.info_chars:
                    return "info", None
                if ch == spec.stdin_char:
                    stdin_flag = True
                if ch in spec.arg_chars:
                    take_next = k == len(t) - 1
                    break
                if ch in spec.attached_chars:
                    break
                k += 1
                if ch in spec.digit_chars:
                    while k < len(t) and t[k] in "0123456789abcdefABCDEFxX":
                        k += 1
            j += 2 if take_next else 1
            continue
        break
    operand = args[j] if j < len(args) else None
    return ("stdin-flag" if stdin_flag else "operand"), operand


GLOB_REASON = ("the command name is built by a glob or a brace expansion, which this hook "
               "does not expand, ")


def _built_by_expansion(word):
    """True when bash may expand word by a glob or a brace expansion: an unquoted *, ?, [
    or { was written in it, or it is a NAME[...] word read as a subscript that is not an
    assignment (bash expands such a word, e[[:alpha:]]v among them, as a pattern), and its
    text holds a *, a ?, a [...] or a {...} with a , or .. in it. Read fail closed: which
    of those characters were quoted is not kept."""
    return ((word.pattern or (word.subscript and not word.assign))
            and GLOB_SHAPE.search(word.text) is not None)


def _fed_standard_input(cmd):
    """True when cmd's standard input is a listed shape, or a word of it is -, a
    standard-input path or a process substitution."""
    if cmd.shape() in STDIN_SHAPES:
        return True
    return any(not isinstance(item, Word) or item.psubs or item.text == "-"
               or item.text in STDIN_PATHS for item in cmd.items)


def _decide_one(cmd, depth=0, strict=True):
    """(argv, reason) when this simple command's interpreter reads its program from stdin.

    A command name built by a glob or a brace expansion is refused, unexpanded, when the
    command's standard input is a listed shape or an argument names standard input. A
    command fed standard input whose command word cannot be determined with certainty
    (Uncertain) is refused, naming the reason, and so are wrappers nested past
    WRAPPER_LEVELS in any command, as are a command word, a wrapper's name or a word a
    wrapper reads built by a glob or a brace expansion and a sudo long option sudo would
    not read as one option. strict False (a
    later word read as a command's start) keeps only those refusals made whatever the
    standard input is.
    """
    try:
        argv = _argv(cmd.items, strict and _fed_standard_input(cmd))
    except Uncertain as exc:
        reason = exc.reason if exc.always else UNCERTAIN_REASON.format(exc.reason)
        return list(cmd.items), reason
    if not argv or not isinstance(argv[0], Word):
        return None
    if _built_by_expansion(argv[0]):
        shape = cmd.shape()
        if shape in STDIN_SHAPES:
            return argv, GLOB_REASON + "while standard input is a " + shape
        if any(not isinstance(arg, Word) or arg.psubs or arg.text == "-"
               or arg.text in STDIN_PATHS for arg in argv[1:]):
            return argv, (GLOB_REASON + "while an argument is -, a standard-input path or a "
                          "process substitution")
    name = os.path.basename(argv[0].text)
    args = argv[1:]
    if name in ("source", "."):
        if args and _text(args[0]) == "--":
            args = args[1:]
        if args and (not isinstance(args[0], Word) or args[0].psubs):
            return argv, "a process substitution is the sourced program"
        if args and args[0].text in STDIN_PATHS:
            return argv, "the sourced path names standard input"
        return None
    spec = _spec_for(name)
    if spec is None:
        return None
    mode, operand = _scan(args, spec)
    if mode == "inline" and spec.shell:
        return _decide_c_string(argv, args, cmd)
    if mode in ("inline", "module", "info"):
        return None
    if mode == "stdin-flag":
        return argv, "-s reads the commands from standard input"
    if mode == "stdin" or (isinstance(operand, Word) and operand.text == "-"):
        return argv, "'-' names standard input as the program"
    if operand is not None and (not isinstance(operand, Word) or operand.psubs):
        return argv, "a process substitution is the program"
    if operand is not None and operand.text in STDIN_PATHS:
        return argv, "the program path names standard input"
    if operand is not None:
        return None
    if not spec.shell:
        return argv, "no script operand, so the program is read from standard input"
    shape = cmd.shape()
    if shape in STDIN_SHAPES:
        return argv, "no script operand while standard input is a " + shape
    return None


# A listed interpreter, source or . named anywhere in a -c string or a here-document body.
INTERPRETER_NAME = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:python(?:\d+(?:\.\d+)*t?)?|perl(?:\d+(?:\.\d+)*)?"
    r"|ruby(?:\d+(?:\.\d+)*)?|php(?:\d+(?:\.\d+)*)?|nodejs|node|r?bash|sh|zsh|dash|source)"
    r"(?![A-Za-z0-9_-])|(?<![^\s;&|(){}`])\.(?![^\s;&|(){}`])")


def _c_string(args):
    """A shell's -c string: its first operand after the options, or None (bash then fails).

    --rcfile and --init-file take the next word; a cluster takes one word for each o or O
    in it, wherever the letter stands; -- and - end the options. A c or s in a cluster that starts
    with + is read as in one that starts with - (bash +c, +s), as bash reads it.
    """
    j = 0
    while j < len(args):
        item = args[j]
        if not isinstance(item, Word):
            return item
        t = item.text
        if t in ("--", "-"):
            return args[j + 1] if j + 1 < len(args) else None
        if t in SHELL.long_args:
            j += 2
        elif t.startswith("--"):
            j += 1
        elif t == "+":
            j += 1
        elif len(t) > 1 and t[0] in "-+":
            j += 1 + _shell_option_arguments(t)
        else:
            return item
    return None


# A token of a -c string or a here-document body for the presence tests: the text between
# blanks, newlines and the shell's operator characters.
_TOKEN = re.compile(r"[^\s;&|()<>{}`,]+")
# Where the words that follow a listed name end: the next command separator.
_SEPARATOR = re.compile(r"[;&|(){}\n]")
# Characters refused together with a listed name in a -c string: a pipe, a redirection, a
# substitution, an expansion, a group or a quote (and every way the text can fail to parse).
_MARKS = ("|", "<", ">", "(", "[", "{", "'", '"', "`")
# The same for an unquoted here-document body, where quotes are plain characters.
_BODY_MARKS = ("$(", "`", "${", "$[")
QUOTING_REASON = ("the -c string holds $'...' or $\"...\" quoting, which this hook does not "
                  "read, so it is refused unread")
OPERATOR_REASON = ("the -c string names an interpreter together with a pipe, a redirection, a "
                   "substitution, a group, a bracket, a brace or a quote, which this hook does "
                   "not read, so it is refused unread")
FORM_REASON = ("the -c string names an interpreter not followed by a script path (as in "
               "python3 -I /abs/s.py), which this hook does not read, so it is refused unread")
BODY_REASON = ("the unquoted here-document body holds a $( or a backtick (or a ${ or $[) "
               "together with an interpreter's name, which this hook does not read, so it is "
               "refused unread")


def _plain_text(text):
    """text with line continuations, backslashes and quotes dropped."""
    return re.sub(r"[\\'\"]", "", text.replace("\\\n", ""))


def _listed_names(text):
    """(kind, the text after it) for each listed name in text, by token.

    kind is "source" (source or .), "shell", "python" or "other"; a token names one when its
    part after the last / does.
    """
    found = []
    for match in _TOKEN.finditer(text):
        base = match.group().rsplit("/", 1)[-1]
        if base in ("source", "."):
            kind = "source"
        else:
            spec = _spec_for(base)
            if spec is None:
                continue
            kind = "shell" if spec.shell else "python" if spec is PYTHON else "other"
        found.append((kind, text[match.end():]))
    return found


def _names_a_listed_name(*texts):
    return any(INTERPRETER_NAME.search(text) or _listed_names(text) for text in texts)


def _body_presence(*texts):
    """True when an unquoted here-document body holds a $(, ${, $[ or backtick and a listed name."""
    return (any(mark in text for text in texts for mark in _BODY_MARKS)
            and _names_a_listed_name(*texts))


def _not_given_a_script(kind, rest, stdin_shape):
    """True when the words after a listed name in a -c string are not a script operand."""
    words = _SEPARATOR.split(rest, maxsplit=1)[0].split()
    if kind == "python" and words[:1] == ["-I"]:
        words = words[1:]
    first = words[0] if words else None
    if first is not None and (first[0] in "-+" or first.startswith(("/dev/", "/proc/"))):
        return True
    if kind == "source":
        return False
    if first is None or first[0] == "#" or any(ch in first for ch in "<>&"):
        return kind != "shell" or stdin_shape
    return False


def _decide_c_string(argv, args, cmd):
    """(argv, reason) when a shell's -c string is refused unread by the presence test.

    The string is never read as commands. It is refused when it holds $'...' or $"..."
    quoting, or names a listed interpreter, source or . together with any of | < > ( [ { ' "
    or a backtick, or not followed by a script path; one bash may receive as other text, and one
    built by expansion that names any of them, is refused unread as well.
    """
    string = _c_string(args)
    if string is None:
        return None
    if not isinstance(string, Word) or string.psubs:
        return argv, "a process substitution is the -c string, which this hook does not read"
    if string.unread:
        return argv, ("the -c string is written with $'...' or $\"...\" quoting or an unquoted "
                      "*, ?, [ or {, which this hook does not read, so it is refused unread")
    text = string.text
    plain = _plain_text(text)
    if "$'" in text or '$"' in text:
        return argv, QUOTING_REASON
    if not _names_a_listed_name(text, plain):
        return None
    if string.dynamic:
        return argv, ("the -c string is built by expansion and names an interpreter, so "
                      "it is refused unread")
    if any(mark in t for t in (text, plain) for mark in _MARKS):
        return argv, OPERATOR_REASON
    stdin_shape = cmd.shape() in STDIN_SHAPES
    if any(_not_given_a_script(kind, rest, stdin_shape) for kind, rest in _listed_names(plain)):
        return argv, FORM_REASON
    return None


RESERVED_AFTER_ASSIGNMENT_REASON = (
    "an assignment is followed in the same simple command by a reserved word, which bash "
    "runs as a command's name, in a command line that feeds standard input to an "
    "interpreter, so it is refused")
SUBSCRIPT_START = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\[")


def _prefix_word(word):
    """True when word may be an assignment prefix: an assignment, or a word that begins NAME[."""
    return word.assign or (not word.quoted and SUBSCRIPT_START.match(word.text) is not None)


def _reserved_inside(token):
    """The first find of _reserved_after_assignment in the substitutions of token (a
    word's $( ), backticks, <( ) and >( ), or a process substitution token), or None."""
    if token is None or token[0] == "OP":
        return None
    if token[0] == "PSUB":
        subs = [token[2]]
    else:
        subs = list(token[1].subs) + [sub for _ch, sub, _keeps in token[1].psubs]
    for sub in subs:
        found = _reserved_after_assignment(sub)
        if found:
            return found
    return None


def _reserved_after_assignment(tokens):
    """The words up to the first reserved word that follows an assignment prefix, or None.

    Read fail closed: a simple command's leading shell words (time -p, time -- and time
    -p -- among them) are skipped; after an assignment prefix every later word counts as in
    command position, a redirection's target excepted; and while a [ in a word after the
    prefix is still open, an operator or a newline does not end the simple command.
    Every substitution is read the same way, in any word and in a redirection's target,
    at any depth.
    """
    led, brackets, words, timing = None, 0, [], None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token[0] == "W":
            word = token[1]
            found = _reserved_inside(token)
            if found:
                return found
            reserved = not word.dynamic and word.text in (ASSIGNED_RESERVED | RESERVED)
            if led is None:
                if (timing == "time" and _bare(word) == "-p") or (timing and _bare(word) == "--"):
                    timing = "-p" if word.text == "-p" else None
                elif reserved and not word.quoted:
                    timing = "time" if word.text == "time" else None
                elif _prefix_word(word):
                    led, words, timing = True, [], None
                else:
                    led, timing = False, None
            elif led and reserved and word.text in ASSIGNED_RESERVED:
                return words + [word]
            if led:
                words.append(word)
                if not reserved:
                    brackets = max(0, brackets + word.text.count("[") - word.text.count("]"))
        elif token[0] == "PSUB":
            found = _reserved_inside(token)
            if found:
                return found
            if led is None:
                led, timing = False, None
        elif token[1] in REDIRECTIONS:
            found = ((isinstance(token[2], Word) and _reserved_inside(("W", token[2])))
                     or _reserved_inside(tokens[i + 1] if i + 1 < len(tokens) else None))
            if found:
                return found
            i += 2
            continue
        elif not (led and brackets):
            led, brackets, words, timing = None, 0, [], None
        i += 1
    return None


def _feeds_an_interpreter(command, found):
    """(argv, reason) of a later word read as a command's start that the rules refuse, or
    True when command names a listed name with a |, <, >(, - or standard-input path, else
    None."""
    for cmd in found:
        items = [item for item in cmd.items if not (
            isinstance(item, Word) and _bare(item) in (ASSIGNED_RESERVED | RESERVED))]
        if not items or not isinstance(items[0], Word) or not _prefix_word(items[0]):
            continue
        for j in range(1, len(cmd.items)):
            if not isinstance(cmd.items[j], Word):
                continue
            later = Simple(cmd.piped)
            later.stdin, later.items = cmd.stdin, cmd.items[j:]
            problem = _decide_one(later, strict=False)
            if problem:
                return problem
    plain = _plain_text(command)
    if not _names_a_listed_name(command, plain):
        return None
    for text in (command, plain):
        if "|" in text or "<" in text or ">(" in text:
            return True
        if any(t == "-" or t in STDIN_PATHS for t in _TOKEN.findall(text)):
            return True
    return None


def _decide_text(command, base, depth):
    """The first refusal among the simple commands of command, or None.

    base is the standard input of the text: False, True for a pipe, or a shape's name.
    When none refuses, an assignment prefix followed by a reserved word is refused in a
    command line that feeds standard input to an interpreter.
    """
    tokens, _end = _lex(command, 0, depth, None)
    found = []
    _commands(tokens, found, base)
    for cmd in found:
        problem = _decide_one(cmd, depth)
        if problem:
            return problem
    words = _reserved_after_assignment(tokens)
    if words:
        feeds = _feeds_an_interpreter(command, found)
        if isinstance(feeds, tuple):
            return feeds
        if feeds:
            return words, RESERVED_AFTER_ASSIGNMENT_REASON
    return None


# Deny by default: the set of characters and quoted forms the reader is trusted to model in
# a command that receives a feed (see DENY BY DEFAULT above).
MODELLED_WORD_CHARACTERS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                     "0123456789_./:=@%+,-")
MODELLED_OPERATOR_CHARACTERS = frozenset("|&;<>")
UNMODELLED_FEEDS = ("|", "<", ">(")
UNMODELLED_CHARACTERS = (
    ("$", "a $ (a variable, a substitution, an arithmetic expansion or $'...' or $\"...\" "
          "quoting)"),
    ("`", "a backtick substitution"),
    ("()", "a ( or ) (a subshell, a process substitution, an arithmetic command, an array, "
           "a function definition, a case pattern or an extended pattern)"),
    ("{}", "a { or } (a group, a brace expansion or a {NAME} descriptor)"),
    ("[]", "a [ or ] (a subscript, a bracket expression or a test)"),
    ("*?", "a glob character"),
    ("!", "a ! (a negation, a history or an extended pattern)"),
    ("~", "a tilde expansion"),
    ("#", "a # (a comment)"),
    ("\\", "a backslash or a line continuation"),
)
# Constructs that can build a word at run time (see DENY BY DEFAULT above).
BUILT_WORD_CONSTRUCTS = {
    "$": "a $ (a variable, a parameter expansion, a substitution, an arithmetic expansion or "
         "$'...' or $\"...\" quoting, quoted or not)",
    "`": "a backtick (a substitution, quoted or not)",
    "glob": "an unquoted glob character (* or ?)",
    "[": "an unquoted bracket expression",
    "brace": "an unquoted brace pattern",
    "extended": "an unquoted extended pattern",
}
# A character that ends the raw text of a word, read for a bracket or brace pattern.
BUILT_WORD_ENDS = frozenset(" \t\n|&;<>()")


def _unmodelled_character(ch):
    for chars, what in UNMODELLED_CHARACTERS:
        if ch in chars:
            return what
    return "a character outside printable ASCII or the modelled set (" + ascii(ch) + ")"


def _unmodelled(command):
    """A description of the first construct in command outside the modelled set, or None."""
    pos, n, pending = 0, len(command), []
    while pos < n:
        ch = command[pos]
        if ch in MODELLED_WORD_CHARACTERS or ch in " \t":
            pos += 1
        elif ch == "'":
            end = command.find("'", pos + 1)
            if end < 0:
                return "an unterminated single quote"
            pos = end + 1
        elif ch == '"':
            end = command.find('"', pos + 1)
            if end < 0:
                return "an unterminated double quote"
            for mark in ("$", "`", "\\"):
                if mark in command[pos + 1:end]:
                    return _unmodelled_character(mark) + " inside double quotes"
            pos = end + 1
        elif ch == "\n":
            pos += 1
            for delimiter, quoted, strip_tabs in pending:
                body_end, after = _skip_body(command, pos, delimiter, strip_tabs)
                body = command[pos:body_end]
                if not quoted and any(mark in body for mark in ("$", "`", "\\")):
                    return ("a $, a backtick or a backslash in a here-document body whose "
                            "delimiter is unquoted")
                pos = after
            pending.clear()
        elif command.startswith("<<", pos) and not command.startswith("<<<", pos):
            pos += 2
            strip_tabs = command.startswith("-", pos)
            pos += 1 if strip_tabs else 0
            while pos < n and command[pos] in " \t":
                pos += 1
            text, quoted = [], False
            while pos < n and command[pos] not in " \t\n|&;<>":
                ch = command[pos]
                if ch in "'\"":
                    end = command.find(ch, pos + 1)
                    if end < 0:
                        return "an unterminated quote in a here-document delimiter"
                    inner = command[pos + 1:end]
                    if ch == '"' and any(mark in inner for mark in ("$", "`", "\\")):
                        return "a $, a backtick or a backslash in a here-document delimiter"
                    text.append(inner)
                    quoted = True
                    pos = end + 1
                elif ch == "\\" and pos + 1 < n and command[pos + 1] != "\n":
                    text.append(command[pos + 1])
                    quoted = True
                    pos += 2
                elif ch in MODELLED_WORD_CHARACTERS:
                    text.append(ch)
                    pos += 1
                else:
                    return _unmodelled_character(ch) + " in a here-document delimiter"
            if not text:
                return "a here-document operator with no delimiter word"
            pending.append(("".join(text), quoted, strip_tabs))
        elif ch in MODELLED_OPERATOR_CHARACTERS:
            pos += 1
        else:
            return _unmodelled_character(ch)
    return None


def _raw_word_rest(command, pos):
    """The raw text from pos to the end of the word it lies in (quotes kept)."""
    end = pos
    while end < len(command) and command[end] not in BUILT_WORD_ENDS:
        end += 1
    return command[pos:end]


def _builds_a_word(command):
    """A description of the first construct in command that can build a word at run time,
    or None.

    Read fail closed: any $ and any backtick count wherever they stand (unquoted, inside
    single or double quotes, after a backslash, in a here-document delimiter or in the body
    of a here-document whose delimiter is unquoted), since quoted text may be read again as
    commands (a -c string, an eval); only the body of a here-document whose delimiter is
    quoted is skipped. A glob character (* or ?), a bracket expression (a [ with a ] later
    in the same word), a brace pattern (a { with a , or .. before a later } in the same
    word) and an extended pattern (one of ? * + @ ! directly before a () count only where
    they are unquoted and not after a backslash."""
    pos, n, pending = 0, len(command), []
    while pos < n:
        ch = command[pos]
        if ch in "$`":
            return BUILT_WORD_CONSTRUCTS[ch]
        if ch == "\\":
            pos += 2
        elif ch in "'\"":
            end = pos + 1
            while end < n and command[end] != ch:
                end += 2 if ch == '"' and command[end] == "\\" else 1
            inner = command[pos + 1:end]
            for mark in "$`":
                if mark in inner:
                    return BUILT_WORD_CONSTRUCTS[mark]
            pos = end + 1
        elif ch == "\n":
            pos += 1
            for delimiter, quoted, strip_tabs in pending:
                body_end, after = _skip_body(command, pos, delimiter, strip_tabs)
                if not quoted:
                    for mark in "$`":
                        if mark in command[pos:body_end]:
                            return BUILT_WORD_CONSTRUCTS[mark]
                pos = after
            pending.clear()
        elif command.startswith("<<", pos) and not command.startswith("<<<", pos):
            pos += 2
            strip_tabs = command.startswith("-", pos)
            pos += 1 if strip_tabs else 0
            while pos < n and command[pos] in " \t":
                pos += 1
            text, quoted = [], False
            while pos < n and command[pos] not in " \t\n|&;<>":
                ch = command[pos]
                if ch in "'\"":
                    end = command.find(ch, pos + 1)
                    end = n if end < 0 else end
                    text.append(command[pos + 1:end])
                    quoted, pos = True, end + 1
                elif ch == "\\":
                    text.append(command[pos + 1:pos + 2])
                    quoted, pos = True, pos + 2
                else:
                    text.append(ch)
                    pos += 1
            pending.append(("".join(text), quoted, strip_tabs))
        elif ch in "?*+@!" and command.startswith("(", pos + 1):
            return BUILT_WORD_CONSTRUCTS["extended"]
        elif ch in "*?":
            return BUILT_WORD_CONSTRUCTS["glob"]
        elif ch == "[" and "]" in _raw_word_rest(command, pos + 1):
            return BUILT_WORD_CONSTRUCTS["["]
        elif ch == "{":
            rest = _raw_word_rest(command, pos + 1)
            inside = rest[:rest.rfind("}")] if "}" in rest else ""
            if "," in inside or ".." in inside:
                return BUILT_WORD_CONSTRUCTS["brace"]
            pos += 1
        else:
            pos += 1
    return None


def _deny_by_default(command, depth=0, functions=None, scope=None):
    """(None, reason) when a command that receives a feed is refused by default, else None.

    The command that receives a feed (a consumer) is the command after a pipe, the command
    a here-document, a here-string, a < redirection or a <( ) process substitution feeds,
    every command inside a >( ), and, read fail closed, every command of a group or compound
    a pipe or a < redirection feeds and every command inside a substitution written in a
    consumer. A consumer is refused when its command word, or a wrapper word before it, can
    build a word at run time; when its command word lies outside the modelled set; or when
    its command word is a listed interpreter, source or . and a word that chooses its
    program (the command word, its options and its program operand, or, with no literal
    program operand, any part of the command) holds a construct outside the modelled set.
    A line whose consumers cannot be located is refused."""
    plain = _plain_text(command)
    if not any(feed in text for text in (command, plain) for feed in UNMODELLED_FEEDS):
        return None
    functions = {**(functions or {}), **_function_bodies(command)}
    scanner = _FeedScanner(command, 0)
    try:
        scanner.scan(0, None)
    except _Unlocated as exc:
        where, built = exc.args[0], _builds_a_word(command)
        if built:
            where += "; the line holds " + built + ", which can build a word at run time"
        return None, CONSUMER_UNLOCATED_REASON.format(where)
    for seg, feed in _consumers(scanner, None):
        problem = _check_consumer(seg, feed, scope or command, depth, functions)
        if problem:
            return problem
    if depth < MAX_DEPTH:
        for cmd in _all_commands(scanner):
            heads = [w for w in cmd.words
                     if not ASSIGNMENT_WORD.match(w) and w not in CONSUMER_SKIPPED]
            text = _run_text(heads) if heads else None
            if text is not None:
                # A -c string, eval text or flock -c string is read as a line of its own.
                problem = _deny_by_default(text, depth + 1, functions)
                if problem:
                    return problem
            if not heads or not _builds_a_word(heads[0]):
                continue
            for raw in heads[1:]:
                if len(raw) > 1 and raw[0] in "'\"" and raw[-1] == raw[0]:
                    problem = _deny_by_default(raw[1:-1], depth + 1, functions)
                    if problem:
                        return problem
    return None


class _Unlocated(Exception):
    """The text cannot be read far enough to locate every command that receives a feed."""


class _Consumer:
    """One simple command as the deny-by-default reading sees it."""

    __slots__ = ("words", "targets", "feeds", "piped", "group", "after_close", "nested",
                 "bodies", "descriptors")

    def __init__(self, piped, group, after_close):
        self.words = []         # raw words, redirection targets excluded
        self.targets = []       # raw redirection targets and here-document delimiters
        self.feeds = []         # each < operator and <( ) written in the command
        self.piped = piped      # the command follows | or |&
        self.group = group      # the command opens a ( ) group that a pipe feeds
        self.after_close = after_close  # the command follows a ) with nothing between
        self.nested = []        # (kind, _FeedScanner) of each substitution written in it
        self.bodies = []        # (body, quoted) of each here-document it reads
        self.descriptors = []   # each {NAME} descriptor written before a redirection


class _FeedScanner:
    """Splits command text into simple commands, quote by quote, to find the feeds.

    Words, quotes, $( ), ${ }, $(( )), $[ ], backticks, <( ) and >( ) are read to their
    ends; the text of a substitution is read as commands of its own, at any depth.
    Operators split commands; a ( or ) is read as an operator; [[ ]] and (( )) at a
    command's start are read as one word. Anything that cannot be read raises _Unlocated.
    """

    def __init__(self, src, depth):
        if depth > MAX_DEPTH:
            raise _Unlocated("nesting deeper than " + str(MAX_DEPTH))
        self.src, self.depth = src, depth
        self.commands = []
        self.cur = None
        self.word = None        # raw text of the word being read
        self.target = None      # the redirection operator whose target is being read
        self.piped = self.group = self.after_close = False
        self.pending = []       # (command, raw delimiter, strip_tabs)
        self.spans = []         # (start, end) of each here-document body and terminator
        self.parens = self.case = 0
        self.test = False       # inside [[ ]]

    def command(self):
        if self.cur is None:
            self.cur = _Consumer(self.piped, self.group, self.after_close)
            self.piped = self.group = self.after_close = False
            self.commands.append(self.cur)
        return self.cur

    def add(self, text):
        self.command()
        self.word = (self.word or "") + text

    def end_word(self):
        if self.word is None:
            return
        raw, self.word = self.word, None
        cmd = self.command()
        if self.target is not None:
            op, self.target = self.target, None
            cmd.targets.append(raw)
            if op in ("<<", "<<-"):
                self.pending.append((cmd, raw, op == "<<-"))
            return
        if raw == "[[" and not cmd.words:
            self.test = True
        elif raw == "]]":
            self.test = False
        elif raw == "case" and not cmd.words:
            self.case += 1
        elif raw == "esac" and self.case:
            self.case -= 1
        cmd.words.append(raw)

    def end_command(self):
        self.end_word()
        if self.target is not None:
            raise _Unlocated("a redirection with no target")
        self.cur = None

    def nested(self, kind, pos, closer):
        inner = _FeedScanner(self.src, self.depth + 1)
        end = inner.scan(pos, closer)
        self.command().nested.append((kind, inner))
        return end

    def dollar_span(self, pos):
        """The end of the $ form at pos; a substitution in it is read as commands."""
        src, n = self.src, len(self.src)
        if src.startswith("$((", pos):
            return self.arith(pos + 3, 2)
        if src.startswith("$(", pos):
            return self.nested("$(", pos + 2, ")")
        if src.startswith("${", pos):
            return self.braces(pos + 2)
        if src.startswith("$[", pos):
            end = src.find("]", pos)
            if end < 0:
                raise _Unlocated("an unterminated $[")
            return end + 1
        if src.startswith("$'", pos):
            end = pos + 2
            while end < n and src[end] != "'":
                end += 2 if src[end] == "\\" else 1
            if end >= n:
                raise _Unlocated("an unterminated $' quote")
            return end + 1
        return pos + 1

    def double_span(self, pos):
        src, n = self.src, len(self.src)
        pos += 1
        while pos < n and src[pos] != '"':
            if src[pos] == "\\":
                pos += 2
            elif src.startswith(("$(", "${", "$["), pos):
                pos = self.dollar_span(pos)
            elif src[pos] == "`":
                pos = self.nested("`", pos + 1, "`")
            else:
                pos += 1
        if pos >= n:
            raise _Unlocated("an unterminated double quote")
        return pos + 1

    def braces(self, pos):
        src, n, depth = self.src, len(self.src), 1
        while pos < n:
            ch = src[pos]
            if ch == "\\":
                pos += 2
            elif ch == "'":
                end = src.find("'", pos + 1)
                if end < 0:
                    raise _Unlocated("an unterminated single quote")
                pos = end + 1
            elif ch == '"':
                pos = self.double_span(pos)
            elif ch == "$":
                pos = self.dollar_span(pos)
            elif ch == "`":
                pos = self.nested("`", pos + 1, "`")
            elif src.startswith(("<(", ">("), pos):
                pos = self.nested(src[pos:pos + 2], pos + 2, ")")
            else:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if not depth:
                        return pos + 1
                pos += 1
        raise _Unlocated("an unterminated ${")

    def arith(self, pos, depth):
        src, n = self.src, len(self.src)
        while pos < n:
            ch = src[pos]
            if ch == "\\":
                pos += 2
            elif src.startswith(("$(", "${"), pos) and not src.startswith("$((", pos):
                pos = self.dollar_span(pos)
            elif ch == "`":
                pos = self.nested("`", pos + 1, "`")
            else:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if not depth:
                        return pos + 1
                pos += 1
        raise _Unlocated("an unterminated arithmetic expression")

    def pattern(self, pos):
        """The end of an extended pattern whose ( ends at pos - 1."""
        src, n, depth = self.src, len(self.src), 1
        while pos < n:
            ch = src[pos]
            if ch == "\\":
                pos += 2
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if not depth:
                    return pos + 1
            pos += 1
        raise _Unlocated("an unterminated extended pattern")

    def bodies(self, pos):
        """Skip the bodies of the here-documents opened on the line that ended at pos."""
        pending, self.pending = self.pending, []
        for cmd, raw, strip_tabs in pending:
            delimiter = re.sub(r"['\"]", "", re.sub(r"\\(.)", r"\1", raw))
            quoted = any(ch in raw for ch in "'\"\\")
            body_end, after = _skip_body(self.src, pos, delimiter, strip_tabs)
            cmd.bodies.append((self.src[pos:body_end], quoted))
            self.spans.append((pos, after))
            if not quoted:
                saved, self.cur = self.cur, cmd
                p = pos
                while p < body_end:
                    if self.src[p] == "\\":
                        p += 2
                    elif self.src.startswith(("$(", "${"), p):
                        p = self.dollar_span(p)
                    elif self.src[p] == "`":
                        p = self.nested("`", p + 1, "`")
                    else:
                        p += 1
                self.cur = saved
            pos = after
        return pos

    def operator(self, pos):
        src = self.src
        for op in FEED_REDIRECTIONS:
            if src.startswith(op, pos):
                if self.word is not None and FD_PREFIX.fullmatch(self.word):
                    if self.word.startswith("{"):
                        self.command().descriptors.append(self.word)
                    self.word = None
                else:
                    self.end_word()
                if self.target is not None:
                    raise _Unlocated("a redirection with no target")
                if op.startswith("<"):
                    self.command().feeds.append(op)
                else:
                    self.command()
                self.target = op
                return pos + len(op)
        for op in FEED_CONTROLS:
            if src.startswith(op, pos):
                self.end_command()
                self.after_close = False
                if op in ("|", "|&"):
                    self.piped = True
                return pos + len(op)
        return None

    def scan(self, pos, closer):
        """Read commands from pos to closer (")" or a backtick) or the end; the end."""
        src, n = self.src, len(self.src)
        while pos < n:
            ch = src[pos]
            if closer == "`" and ch == "`":
                self.end_command()
                return pos + 1
            if ch == ")" and not self.test and not self.case:
                if self.parens:
                    self.parens -= 1
                    self.end_command()
                    self.after_close = True
                    pos += 1
                    continue
                if closer == ")":
                    self.end_command()
                    return pos + 1
            if ch in " \t":
                self.end_word()
                pos += 1
            elif ch == "\n":
                self.end_command()
                self.after_close = False
                pos = self.bodies(pos + 1)
            elif ch == "#" and self.word is None:
                end = src.find("\n", pos)
                pos = n if end < 0 else end
            elif ch == "\\":
                if not src.startswith("\\\n", pos):
                    self.add(src[pos:pos + 2])
                pos += 2
            elif ch == "'":
                end = src.find("'", pos + 1)
                if end < 0:
                    raise _Unlocated("an unterminated single quote")
                self.add(src[pos:end + 1])
                pos = end + 1
            elif ch == '"':
                end = self.double_span(pos)
                self.add(src[pos:end])
                pos = end
            elif ch == "$":
                end = self.dollar_span(pos)
                self.add(src[pos:end])
                pos = end
            elif ch == "`":
                end = self.nested("`", pos + 1, "`")
                self.add(src[pos:end])
                pos = end
            elif src.startswith(("<(", ">("), pos):
                kind = src[pos:pos + 2]
                if kind == "<(":
                    self.command().feeds.append(kind)
                end = self.nested(kind, pos + 2, ")")
                self.add(src[pos:end])
                pos = end
            elif (src.startswith("((", pos) and self.word is None and self.target is None
                  and all(w in RESERVED for w in (self.cur.words if self.cur else []))):
                end = self.arith(pos + 2, 2)
                self.add(src[pos:end])
                pos = end
            elif self.test and ch in "<>|&()":
                self.add(ch)
                pos += 1
            elif ch == "(" and self.word and self.word[-1] in "?*+@!":
                end = self.pattern(pos + 1)
                self.add(src[pos:end])
                pos = end
            elif ch == "(":
                prev = self.cur
                self.end_command()
                self.group = self.piped or (prev is not None and (prev.piped or prev.group))
                self.parens += 1
                pos += 1
            elif ch == ")":
                self.end_command()
                pos += 1
            else:
                end = self.operator(pos)
                if end is None:
                    self.add(ch)
                    pos += 1
                else:
                    pos = end
        if closer is not None:
            raise _Unlocated("an unterminated substitution")
        self.end_command()
        if self.piped:
            raise _Unlocated("a pipe with no command after it")
        return n


# Read longest first, so <<< is not read as << and <.
FEED_REDIRECTIONS = ("&>>", "<<<", "<<-", "&>", "<<", "<&", "<>", ">>", ">&", ">|", "<", ">")
FEED_CONTROLS = (";;&", "||", "&&", "|&", ";;", ";&", "|", ";", "&")
# A descriptor written directly before a redirection operator: digits or {NAME}.
FD_PREFIX = re.compile(r"[0-9]+|\{[A-Za-z_][A-Za-z0-9_]*(?:\[.*\])?\}", re.S)
ASSIGNMENT_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\[[^\]]*\])?\+?=")
# Shell words skipped before a consumer's command word, and words after which no word of
# the same simple command is a command.
CONSUMER_SKIPPED = frozenset(("!", "then", "do", "else", "elif", "if", "while", "until", "{",
                              "}", "done", "fi", "esac", "coproc"))
CONSUMER_NOT_COMMANDS = frozenset(("for", "case", "select", "function", "in", "[["))
# A group or compound whose every command a feed into it reaches.
CONSUMER_COMPOUNDS = frozenset(("if", "while", "until", "for", "case", "select", "{",
                                "function", "coproc"))
CONSUMER_CLOSERS = frozenset(("}", "done", "fi", "esac"))
CONSUMER_WRAPPERS = WRAPPERS | frozenset(("xargs", "eval", "stdbuf", "setsid", "ionice",
                                          "flock", "busybox", "builtin"))
# Feeds that are a named file: an interpreter given no program operand reads that file, a
# residual stated below, not a feed whose text the command line holds.
FILE_FEEDS = frozenset(("<", "<&", "<>"))
XARGS_ARGUMENT_CHARS = "adEILnPs"
# --max-lines (and --replace, --eof) take an optional argument that must be attached.
XARGS_LONG_ARGUMENTS = frozenset(("--arg-file", "--delimiter", "--max-args", "--max-procs",
                                  "--max-chars", "--process-slot-var"))
RUNNER_OPTIONS = {
    "stdbuf": ("ioe", frozenset(("--input", "--output", "--error"))),
    "setsid": ("", frozenset()),
    "ionice": ("cnpPu", frozenset(("--class", "--classdata", "--pid", "--pgid", "--uid"))),
    "flock": ("Ew", frozenset(("--conflict-exit-code", "--timeout", "--wait"))),
}
FLOCK_COMMAND = ("-c", "--command")
# A path under /dev/fd/ or /proc/*/fd/, or /dev/stdin, /dev/stdout or /dev/stderr, read
# after repeated slashes and . parts are dropped.
DESCRIPTOR_PATH = re.compile(r"(?:^|/)dev/(?:fd(?:/|$)|std)|(?:^|/)proc/[^/]+/fd(?:/|$)")
# A function definition's head: function NAME, function NAME (), or NAME ().
FUNCTION_HEAD = re.compile(r"(?<![^\s;&|(){}])(?:function\s+([A-Za-z0-9_.:-]+)(?:\s*\(\s*\))?"
                           r"|([A-Za-z0-9_.:-]+)\s*\(\s*\))")
# What opens or closes a level before an assignment, read fail closed.
LEVEL_MARKS = re.compile(r"(?<![^\s;&|(){}])(?:if|while|until|for|select|case|fi|done|esac)"
                         r"(?![^\s;&|(){}])|[(){}]")
LEVEL_OPENS = frozenset(("if", "while", "until", "for", "select", "case", "(", "{"))
FEED_NAMES = {"|": "a pipe", "<": "a < redirection", "<<": "a here-document",
              "<<-": "a here-document", "<<<": "a here-string", "<&": "a < redirection",
              "<>": "a < redirection", "<(": "a <( ) process substitution",
              ">(": "a >( ) process substitution",
              "inherited": "the feed into the group, compound or substitution it is written in"}
CONSUMER_BUILT_REASON = ("the command that receives {} has its command word, or a wrapper word "
                         "before it, written with {}, which can build a word at run time, an "
                         "interpreter's name among them, so the line is refused by default")
CONSUMER_WORD_REASON = ("the command that receives {} has a command word, or a wrapper's name, "
                        "holding {}, outside the set this hook's reader is trusted to model, "
                        "so the line is refused by default")
CONSUMER_INTERPRETER_REASON = ("the command that receives {} is the interpreter {} and holds {}, "
                               "a construct this hook's reader is not trusted to model, so not "
                               "every word of it is known to have been read and the line is "
                               "refused by default")
CONSUMER_STDIN_REASON = ("the command that receives {} is the interpreter {} with no literal "
                         "program operand, so it may read its program from that feed, and "
                         "the line is refused by default")
CONSUMER_UNLOCATED_REASON = ("the line feeds standard input, and the command that receives the "
                             "feed cannot be located ({}), so the line is refused by default")


def _first_word(cmd):
    for raw in cmd.words:
        if not ASSIGNMENT_WORD.match(raw):
            return raw
    return None


def _feeds_the_level(cmd):
    """True when cmd's < feed reaches every command of its level, read fail closed: a
    redirection of a group or compound (after ), }, done, fi or esac), a command of
    redirections only, or an exec given only redirections and options."""
    if not cmd.feeds or not any(f != "<(" for f in cmd.feeds):
        return False
    first = _first_word(cmd)
    if first is None or cmd.after_close or first in CONSUMER_CLOSERS:
        return True
    words = [w for w in cmd.words if not ASSIGNMENT_WORD.match(w)]
    return words[0] == "exec" and all(w.startswith("-") for w in words[1:])


def _compound_marks(cmd):
    """(opening words, closing words) cmd holds where bash reads a command's start."""
    opens = closes = 0
    words, i = cmd.words, 0
    while i < len(words):
        raw = words[i]
        if ASSIGNMENT_WORD.match(raw):
            break
        if raw in CONSUMER_COMPOUNDS:
            opens += 1
            if raw in ("for", "case", "select"):
                break
            i += 2 if raw in ("function", "coproc") else 1
        elif raw in CONSUMER_CLOSERS:
            closes += 1
            i += 1
        elif raw in CONSUMER_SKIPPED or raw == "time":
            i += 1
        else:
            break
    return opens, closes


def _feed_key(cmd):
    """The feed cmd's < operators and <( ) give it, a here-document, a here-string or a
    process substitution before a file."""
    for key in ("<<<", "<<", "<<-", "<(", "<", "<&", "<>"):
        if key in cmd.feeds:
            return key
    return None


def _all_commands(scanner):
    for cmd in scanner.commands:
        yield cmd
        for _kind, inner in cmd.nested:
            yield from _all_commands(inner)


def _consumers(scanner, inherited):
    """(command, feed) for each command of scanner's level, and of the levels nested in
    it, that receives a feed."""
    whole = inherited or next((_feed_key(c) for c in scanner.commands
                               if _feeds_the_level(c)), None)
    compound, depth = None, None
    for cmd in scanner.commands:
        feed = (("|" if cmd.piped or cmd.group else _feed_key(cmd) if cmd.feeds else None)
                or compound or whole)
        opens, closes = _compound_marks(cmd)
        if feed and not compound and (cmd.group or opens):
            # A ( ) group or a case compound (whose patterns end in a ) of their own) is
            # read as reaching the end of its level; any other keyword compound ends at the
            # closing word that matches it.
            compound, depth = feed, (None if cmd.group or "case" in cmd.words else 0)
        if compound and depth is not None:
            depth += opens - closes
        if feed:
            yield cmd, feed
        if compound and depth is not None and depth <= 0:
            compound, depth = None, None
        for kind, inner in cmd.nested:
            yield from _consumers(inner, ">(" if kind == ">(" else
                                  "inherited" if feed else None)


def _after_options(args, short_args, long_args):
    """args after a runner's options: a long option in long_args takes the next word, and
    the first letter of a cluster found in short_args takes the rest of the word or else
    the next word."""
    j = 0
    while j < len(args):
        t = _text(args[j])
        if t == "--":
            return args[j + 1:]
        if t.startswith("--"):
            j += 2 if t in long_args else 1
        elif len(t) > 1 and t[0] == "-":
            k = next((k for k in range(1, len(t)) if t[k] in short_args), None)
            j += 2 if k == len(t) - 1 else 1
        else:
            break
    return args[j:]


def _after_xargs(args):
    return _after_options(args, XARGS_ARGUMENT_CHARS, XARGS_LONG_ARGUMENTS)


def _after_flock(items):
    """flock's words after its options and its lock file or descriptor.

    _after_options reads every word before the lock file that starts with - as an option,
    so a -c or --command there, alone or in a cluster such as -nc, lands among the
    options, where this reading does not place flock's command: it is refused as
    unlocated (``cat x | flock -c /abs/lock grep y``). A -c after the lock file is left
    at the front of the words returned, and the callers read the word after it.
    """
    short_args, long_args = RUNNER_OPTIONS["flock"]
    rest = _after_options(items, short_args, long_args)
    options = items[:len(items) - len(rest)]
    if any(_text(o) in FLOCK_COMMAND or (_text(o)[:1] == "-" and _text(o)[1:2] != "-"
                                          and "c" in _text(o)) for o in options):
        raise Uncertain("a flock -c written among its options")
    return rest[1:]


def _after_wrapper(name, items):
    if name == "env":
        return _after_env(items)
    if name == "command":
        j = 0
        while j < len(items) and items[j].text.startswith("-") and items[j].text != "-":
            j += 1
            if items[j - 1].text == "--":
                break
        return items[j:]
    if name == "exec":
        return _skip_cluster(items, "a")
    if name == "nice":
        return _after_nice(items)
    if name == "timeout":
        return _after_timeout(items)
    if name == "nohup":
        return _skip_options(items)
    if name == "sudo":
        return _skip_assignments(_after_sudo(items))
    if name == "xargs":
        return _after_xargs(items)
    if name in ("eval", "builtin"):
        return items[1:] if items and items[0].text == "--" else items
    if name == "busybox":
        return items
    if name == "flock":
        return _after_flock(items)
    if name in RUNNER_OPTIONS:
        return _after_options(items, *RUNNER_OPTIONS[name])
    return _skip_options(items, ("-f", "-o", "--format", "--output"))


def _set_once(command, raw):
    """The literal value of a variable that raw names alone ($NAME, ${NAME}, "$NAME" or
    "${NAME}"), when the line sets it exactly once, earlier, by an assignment word whose
    value is literal modelled text that names no option and no standard-input path, and
    the name appears nowhere else in the line except where it is expanded; else None.
    Read fail closed: a name the line may set any other way (read, for, export, a function,
    eval) appears elsewhere, so it is not resolved."""
    match = VARIABLE_WORD.fullmatch(raw)
    if not match:
        return None
    name = match.group(1) or match.group(2)
    # Quoted text sets nothing: a single-quoted string is dropped, and a double-quoted one
    # is kept only for the $NAME and ${NAME} expansions in it. A line that may run text as
    # commands in this shell (eval, source or .) resolves nothing.
    outside = _outside_quotes(command)
    if re.search(r"(?<![^\s;&|(){}])(?:eval|source|[.])(?![^\s;&|(){}])", outside):
        return None
    sets = list(re.finditer(r"(?<![^\s;&|(){}])" + name + r"=([^\s;&|<>()]*)", outside))
    uses = [m.start() for m in re.finditer(r"[$][{]?" + name + r"(?![A-Za-z0-9_])", outside)]
    if len(sets) != 1 or not uses or sets[0].start() > min(uses):
        return None
    # The assignment sets the variable in this shell only as a simple command of its own
    # at the top level: not a prefix to a command word, not in a ( ), $( ), backtick,
    # group, compound or function, not a pipeline stage, not after && or || and not in
    # the background. Here-document bodies are blanked first: text in one sets nothing.
    source = _without_bodies(command)
    if source is None:
        return None
    outside = _outside_quotes(source)
    sets = list(re.finditer(r"(?<![^\s;&|(){}])" + name + r"=([^\s;&|<>()]*)", outside))
    uses = [m.start() for m in re.finditer(r"[$][{]?" + name + r"(?![A-Za-z0-9_])", outside)]
    if (len(sets) != 1 or not uses or sets[0].start() > min(uses)
            or not _top_level_assignment(outside, sets[0].start(), sets[0].end())):
        return None
    value = sets[0].group(1)
    if (not value or value.startswith("-") or value in STDIN_PATHS
            or not set(value) <= MODELLED_WORD_CHARACTERS):
        return None
    mentions = re.findall(r"(?<![A-Za-z0-9_])" + name + r"(?![A-Za-z0-9_])", outside)
    return value if len(mentions) == 1 + len(uses) else None


def _without_bodies(command):
    """command with each here-document body and terminator line blanked (newlines kept),
    or None when the text cannot be read."""
    scanner = _FeedScanner(command, 0)
    try:
        scanner.scan(0, None)
    except _Unlocated:
        return None
    text, stack = list(command), [scanner]
    while stack:
        current = stack.pop()
        for start, end in current.spans:
            for k in range(start, min(end, len(text))):
                if text[k] != "\n":
                    text[k] = " "
        for cmd in current.commands:
            stack.extend(inner for _kind, inner in cmd.nested)
    return "".join(text)


def _top_level_assignment(outside, start, end):
    """True when outside[start:end] is an assignment-only simple command at the top level
    of the current shell, read fail closed."""
    before = outside[:start].rstrip(" \t")
    if before and not (before.endswith("\n")
                       or (before.endswith(";") and not before.endswith(";;"))
                       or (before.endswith("&")
                           and not before.endswith(("&&", "|&", ">&", "<&")))):
        return False
    after = outside[end:].lstrip(" \t")
    if after and not (after.startswith(("\n", "&&", "||"))
                      or (after.startswith(";") and not after.startswith((";;", ";&")))):
        return False
    depth = 0
    for mark in LEVEL_MARKS.findall(outside[:start]):
        depth += 1 if mark in LEVEL_OPENS else -1
    return depth == 0 and outside[:start].count("`") % 2 == 0


def _masked(command):
    """command with each quoted string and backslash escape, quotes included, replaced by
    as many underscores (positions kept)."""
    out, pos, n = list(command), 0, len(command)
    while pos < n:
        ch = command[pos]
        if ch == "\\":
            end = min(pos + 2, n)
        elif ch == "'":
            end = command.find("'", pos + 1)
            end = n if end < 0 else end + 1
        elif ch == '"':
            end = pos + 1
            while end < n and command[end] != '"':
                end += 2 if command[end] == "\\" else 1
            end = min(end + 1, n)
        else:
            pos += 1
            continue
        out[pos:end] = "_" * (end - pos)
        pos = end
    return "".join(out)


def _function_bodies(command):
    """{name: body text} for each function the line defines; a body that is not a { } or
    ( ) group is read as the rest of the line, and a name defined twice keeps both."""
    masked, found = _masked(command), {}
    for match in FUNCTION_HEAD.finditer(masked):
        name = match.group(1) or match.group(2)
        start, n = match.end(), len(masked)
        while start < n and masked[start] in " \t\n":
            start += 1
        end = n
        if start < n and masked[start] in "{(":
            opener = masked[start]
            closer = "}" if opener == "{" else ")"
            level, k = 0, start
            while k < n:
                if masked[k] == opener:
                    level += 1
                elif masked[k] == closer:
                    level -= 1
                    if not level:
                        end = k
                        break
                k += 1
            start += 1
        found[name] = (found[name] + "\n" if name in found else "") + command[start:end]
    return found


def _dequoted(raw):
    """raw with its quotes removed as the shell removes them; text that cannot be split is
    read with every quote and backslash dropped."""
    try:
        return " ".join(shlex.split(raw.replace("\\\n", "")))
    except ValueError:
        return _plain_text(raw)


def _descriptor_path(text):
    """True when text names a descriptor path in any spelling (DESCRIPTOR_PATH)."""
    parts = [p for p in text.split("/") if p not in ("", ".")]
    return bool(DESCRIPTOR_PATH.search(("/" if text.startswith("/") else "") + "/".join(parts)))


def _read_as_fed(text, key, depth, functions, scope=None):
    """The deny-by-default reading of text as a line of its own in which every command
    receives the feed key names (a < from a named file kept as one); with no key, the
    text is read as it stands. scope is the line whose assignments resolve a variable
    program operand (a function body runs in the shell of the line that defines it)."""
    if depth + 1 > MAX_DEPTH:
        return None, CONSUMER_UNLOCATED_REASON.format("nesting deeper than " + str(MAX_DEPTH))
    if key is None:
        line = text
    elif key in FILE_FEEDS:
        # An exec of redirections only gives every later command of its level the feed.
        line = "exec < /dev/null\n" + text
    else:
        line = ": | { " + text + "\n}"
    return _deny_by_default(line, depth + 1, functions, scope)


def _run_text(words):
    """The text a command runs as a shell line of its own, or None: the -c string of a
    listed shell, the joined operands of eval or a flock -c string, past the wrappers the
    deny-by-default reading models."""
    i, levels = 0, 0
    while i < len(words) and levels <= WRAPPER_LEVELS:
        name = _plain_text(words[i]).rsplit("/", 1)[-1]
        rest = words[i + 1:]
        if name == "eval":
            operands = rest[1:] if rest and _plain_text(rest[0]) == "--" else rest
            return " ".join(_dequoted(r) for r in operands)
        items = [_plain(_plain_text(r)) for r in rest]
        if name in CONSUMER_WRAPPERS:
            try:
                after = _after_wrapper(name, items)
            except (Uncertain, ParseError):
                return None
            raws = {id(item): r for r, item in zip(rest, items)}
            words, i = [raws.get(id(item), item.text) for item in after], 0
            if (name == "flock" and len(words) > 1
                    and _plain_text(words[0]) in FLOCK_COMMAND):
                return _dequoted(words[1])
            levels += 1
            continue
        spec = _spec_for(name)
        if spec is None or not spec.shell or _scan(items, spec)[0] != "inline":
            return None
        found = _c_string(items)
        raw = next((r for r, item in zip(rest, items) if item is found), None)
        return None if raw is None else _dequoted(raw)
    return None


def _outside_quotes(command):
    """command read left to right with each single-quoted string blanked, each double-quoted
    string reduced to the $NAME and ${NAME} expansions in it, and each backslash escape
    blanked."""
    out, pos, n = [], 0, len(command)
    while pos < n:
        ch = command[pos]
        if ch == "\\":
            out.append("  ")
            pos += 2
        elif ch == "'":
            end = command.find("'", pos + 1)
            end = n if end < 0 else end
            out.append(" ")
            pos = end + 1
        elif ch == '"':
            end = pos + 1
            while end < n and command[end] != '"':
                end += 2 if command[end] == "\\" else 1
            inner = command[pos + 1:end]
            out.append(" " + " ".join(re.findall(r"[$][{]?[A-Za-z_][A-Za-z0-9_]*[}]?", inner))
                       + " ")
            pos = end + 1
        else:
            out.append(ch)
            pos += 1
    return "".join(out)


def _program_index(items, spec):
    """The index of the word after the option that gives an inline program or a module
    name (the program, or the first word after an attached one), or None."""
    for k, item in enumerate(items):
        t = item.text
        if t == "--" or not t.startswith("-"):
            return None
        if t in spec.inline or (spec.inline_prefixes and t.startswith(spec.inline_prefixes)):
            return k + 1
        if t.startswith("--") or not spec.cluster:
            continue
        for ch in t[1:]:
            if ch in spec.inline_chars or ch in spec.module_chars:
                return k + 1
            if ch in spec.arg_chars or ch in spec.attached_chars:
                break
    return None


VARIABLE_WORD = re.compile(r'"?\$(?:([A-Za-z_][A-Za-z0-9_]*)|\{([A-Za-z_][A-Za-z0-9_]*)\})"?')


def _check_consumer(cmd, feed, command="", depth=0, functions=None):
    """(None, reason) when the command that receives a feed is refused by default."""
    key, feed = feed, FEED_NAMES.get(feed, "a feed")
    words, i = list(cmd.words), 0
    while i < len(words):
        raw = words[i]
        if ASSIGNMENT_WORD.match(raw) and "[" in raw.split("=", 1)[0]:
            return None, CONSUMER_WORD_REASON.format(
                feed, "an assignment to an array subscript before its command word")
        if ASSIGNMENT_WORD.match(raw) or raw in CONSUMER_SKIPPED:
            i += 1
        elif raw == "time":
            i += 1
            for option in ("-p", "--"):
                if i < len(words) and words[i] == option:
                    i += 1
        elif raw == "function":
            i += 2              # function NAME: the body after it is read as commands
        elif raw in CONSUMER_NOT_COMMANDS:
            return None
        else:
            break
    if i < len(words) and words[i].startswith("(("):
        # An arithmetic command builds no command word: a $NAME, a $# or a +( in it is
        # arithmetic. A substitution in it, read as a command of its own as well, is
        # refused here, fail closed.
        sub = next((mark for mark in ("$(", "`") if mark in words[i]), None)
        if sub:
            return None, CONSUMER_BUILT_REASON.format(feed, BUILT_WORD_CONSTRUCTS[sub[0]])
        if _names_a_listed_name(words[i]):
            return None, CONSUMER_WORD_REASON.format(
                feed, "an arithmetic command that names an interpreter")
        if i == len(words) - 1:
            return None         # an arithmetic command runs no command
        return None, CONSUMER_WORD_REASON.format(feed, "an arithmetic command")
    levels = 0
    while i < len(words):
        raw = words[i]
        if raw == "[":
            return None         # the test command
        built = _builds_a_word(raw)
        if built:
            return None, CONSUMER_BUILT_REASON.format(feed, built)
        what = _unmodelled(raw)
        if what:
            return None, CONSUMER_WORD_REASON.format(feed, what)
        name = _plain_text(raw).rsplit("/", 1)[-1]
        if name not in CONSUMER_WRAPPERS:
            break
        levels += 1
        if levels > WRAPPER_LEVELS:
            return None, DEPTH_REASON
        rest = words[i + 1:]
        if name == "eval":
            # eval joins its operands and reads them again as shell text: they are read as
            # a line of their own in which every command receives this feed.
            for r in rest:
                built = _builds_a_word(r)
                if built:
                    return None, CONSUMER_BUILT_REASON.format(feed, built)
            operands = rest[1:] if rest and _plain_text(rest[0]) == "--" else rest
            return _read_as_fed(" ".join(_dequoted(r) for r in operands), key, depth,
                                functions)
        items = [_plain(_plain_text(r)) for r in rest]
        try:
            after = _after_wrapper(name, items)
        except (Uncertain, ParseError) as exc:
            return None, CONSUMER_UNLOCATED_REASON.format(
                getattr(exc, "reason", None) or str(exc))
        kept = {id(item) for item in after}
        for r, item in zip(rest, items):
            if id(item) not in kept:
                built = _builds_a_word(r)
                if built:
                    return None, CONSUMER_BUILT_REASON.format(feed, built)
        raws = {id(item): r for r, item in zip(rest, items)}
        words, i = [raws.get(id(item), item.text) for item in after], 0
        if name == "flock" and words and _plain_text(words[0]) in FLOCK_COMMAND:
            # flock FILE -c TEXT runs TEXT as a shell line with this feed.
            if len(words) < 2:
                return None
            built = _builds_a_word(words[1])
            if built:
                return None, CONSUMER_BUILT_REASON.format(feed, built)
            return _read_as_fed(_dequoted(words[1]), key, depth, functions)
    if i >= len(words):
        return None
    name = _plain_text(words[i]).rsplit("/", 1)[-1]
    spec = _spec_for(name)
    if (spec is None and name not in ("source", ".") and functions and name in functions
            and "/" not in words[i]):
        # A function the line defines runs its body with this feed.
        return _read_as_fed(functions[name], key, depth, functions, command)
    if spec is not None or name in ("source", "."):
        words = words[:i + 1] + [_set_once(command, r) or r for r in words[i + 1:]]
    if name not in ("source", ".") and spec is None:
        return None
    # The words that choose the program: the interpreter's options and its program operand.
    # Words after a literal program operand, redirection targets and here-document bodies
    # are data for that program and are not read here.
    items = [_plain(_plain_text(r)) for r in words[i + 1:]]
    if spec is None:
        mode, operand = "operand", next((w for w in items if w.text != "--"), None)
    else:
        mode, operand = _scan(items, spec)
    index = next((k for k, item in enumerate(items) if item is operand), None)
    if mode == "info":
        return None             # an informational call reads no program
    if spec is not None and spec.shell and mode == "inline":
        # A listed shell's -c string is read as a line of its own with the feed the shell
        # inherits.
        found = _c_string(items)
        raw = next((r for r, item in zip(words[i + 1:], items) if item is found), None)
        if raw is not None:
            problem = _read_as_fed(_dequoted(raw), key, depth, functions)
            if problem:
                return problem
    if mode == "operand" and index is not None and _descriptor_path(items[index].text):
        # A descriptor path is no literal program operand: it may name this feed.
        mode, index = "descriptor", None
    if mode in ("inline", "module") and spec is not None:
        index = _program_index(items, spec)
        mode = "operand" if index is not None else mode
    if mode == "operand" and index is not None:
        what = _unmodelled(" ".join(cmd.descriptors + words[i:i + index + 2]))
        if what is None:
            return None
        return None, CONSUMER_INTERPRETER_REASON.format(feed, name, what)
    if key not in FILE_FEEDS or mode in ("stdin", "stdin-flag"):
        return None, CONSUMER_STDIN_REASON.format(feed, name)
    what = _unmodelled(" ".join(cmd.words + cmd.targets))
    if what is None:
        for body, quoted in cmd.bodies:
            if not quoted and any(mark in body for mark in ("$", "`", "\\")):
                what = ("a $, a backtick or a backslash in a here-document body whose "
                        "delimiter is unquoted")
                break
    if what is None:
        return None
    return None, CONSUMER_INTERPRETER_REASON.format(feed, name, what)


def decide(command):
    """None to allow; (argv, reason) to refuse, with argv None for unreadable text."""
    try:
        problem = _decide_text(command, False, 0)
    except Refused as exc:
        return exc.problem
    except ParseError as exc:
        return None, "the command text could not be parsed (" + str(exc) + ")"
    if problem:
        return problem
    return _deny_by_default(command)


def _printable(text):
    """Escape each character that is neither printable nor a space separator."""
    return "".join(ch if ch.isprintable() or unicodedata.category(ch) == "Zs"
                   else ascii(ch)[1:-1] for ch in text)


def render(problem):
    argv, reason = problem
    if argv is None:
        what = (reason + ", so whether an interpreter reads its program from standard input "
                "cannot be decided, and this hook fails closed.")
        extra = " If the text is meant as a plain command, balance its quotes, substitutions and groups."
    else:
        shown = _printable(" ".join(_text(item) for item in argv))
        if len(shown) > 160:
            shown = shown[:157] + "..."
        what = "`" + shown + "`: " + reason + "."
        extra = ""
    return ("BLOCKED (stdin-interpreter): " + what + "\n"
            "WHY: a program fed on standard input (a here-document, a here-string, a pipe, '-' "
            "or a process substitution) is not in the command text, so no command-text hook "
            "can check what it runs, and an empty or cut-short feed runs nothing without "
            "saying so.\n"
            "CONSIDER INSTEAD: write the program to a script file under your scratch and run "
            "that file by its path (for example python3 -I /abs/path/script.py or bash "
            "/abs/path/run.sh); a -c or -e program stays with its own hooks' rules." + extra)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict) or payload.get("tool_name", "Bash") != "Bash":
            return 0
        command = (payload.get("tool_input") or {}).get("command") or ""
        if not isinstance(command, str):
            return 0
    except Exception:
        return 0                    # a malformed payload fails open, as in every hook
    try:
        problem = decide(command)
        if not problem:
            return 0
        message = render(problem)
    except Exception as exc:        # a reader that stops part way fails closed
        message = render((None, "reading the command text raised an unexpected "
                          + type(exc).__name__))
    print(message, file=sys.stderr)
    return 2


# (command, should_block). The same cases as StdinInterpreterHookTests in
# .claude/skills/corpus-management/tests/test_linters.py, which checks that they match.
SELF_TEST = [
    ("python3 -I - <<'EOF'\nprint(1)\nEOF", True),
    ("python3 -I - <<'EOF'\nEOF", True),
    ("python3 -I - <<'EOF'", True),
    ('python3', True),
    ("printf 'print(1)' | python3 -I", True),
    ('python <<EOF\nprint(1)\nEOF', True),
    ('python3.14 -I -', True),
    ("/usr/bin/python3 -I - <<<'print(1)'", True),
    ('python3 -I -- -', True),
    ('python3 -W ignore -X dev -', True),
    ("python3 /dev/stdin <<'EOF'\nprint(1)\nEOF", True),
    ('python3 <(cat /abs/gen.py)', True),
    ('env -i PATH=/usr/bin python3 -', True),
    ("env -S 'python3 -I -' <<'EOF'\nEOF", True),
    ('command -p python3 -', True),
    ('exec -a name python3 -', True),
    ('nice -n 5 python3 -', True),
    ('timeout -s KILL -k 5 60 python3 -I -', True),
    ('sudo -u nobody python3 -', True),
    ('nohup python3 -', True),
    ('time -p python3 -', True),
    ("A='x y' python3 -", True),
    ("perl - <<'EOF'\nprint 1;\nEOF", True),
    ("perl -w <<'EOF'\nprint 1;\nEOF", True),
    ("ruby - <<<'puts 1'", True),
    ("printf 'puts 1' | ruby", True),
    ("node - <<<'1'", True),
    ("printf '1' | node", True),
    ("php - <<<'<?php echo 1;'", True),
    ("php <<'EOF'\n<?php echo 1;\nEOF", True),
    ("bash -s -- arg <<'EOF'\necho hi\nEOF", True),
    ('sh -xs', True),
    ("bash <<'EOF'\necho hi\nEOF", True),
    ("sh <<<'echo hi'", True),
    ('cat /abs/run.sh | zsh', True),
    ('dash <<EOF\necho hi\nEOF', True),
    ('cat /abs/run.sh | (bash)', True),
    ('cat /abs/run.sh | { bash; }', True),
    ('bash < <(cat /abs/run.sh)', True),
    ("bash /dev/fd/0 <<<'echo hi'", True),
    ('bash <(cat /abs/run.sh)', True),
    ('sh <(cat /abs/run.sh)', True),
    ('source <(cat /abs/env.sh)', True),
    ('. <(cat /abs/env.sh)', True),
    ("source /dev/stdin <<<'x=1'", True),
    ('cd /abs && python3 -', True),
    ("cat > /abs/gen.py <<'EOF'\nprint(1)\nEOF\npython3 - < /abs/gen.py", True),
    ('echo "$(python3 - <<<\'print(1)\')"', True),
    ('x=`cat /abs/a | bash`', True),
    ('while true; do python3 -; done', True),
    ('cat /abs/run.sh |\nbash', True),
    ('cat /abs/run.sh | # feed\n  bash', True),
    ('cat /abs/run.sh | while true; do bash; break; done', True),
    ('cat /abs/run.sh | until false; do bash; break; done', True),
    ('cat /abs/run.sh | for i in 1; do bash; done', True),
    ('cat /abs/run.sh | if true; then bash; fi', True),
    ('cat /abs/run.sh | while true; do { bash; }; break; done', True),
    ('cat /abs/run.sh | while true; do while false; do :; done; bash; done', True),
    ('source -- <(cat /abs/env.sh)', True),
    ('. -- <(cat /abs/env.sh)', True),
    ('python3.13t -I -', True),
    ('python3t -I -', True),
    ('env -iC /tmp python3 -', True),
    ('env -iu HOME python3 -', True),
    ("env -iS 'python3 -I -'", True),
    ('cat /abs/run.sh | while true; do select y in a; do break; done; bash; break; done', True),
    ('cat /abs/run.sh | for i in 1; do select y in a; do break; done; bash; done', True),
    ('cat /abs/run.sh | (case x in x) :;; esac; bash)', True),
    ('cat /abs/run.sh | ( (case x in x) :;; esac); bash )', True),
    ('cat /abs/run.sh | (case x in x) :;; esac\nbash)', True),
    ('cat /abs/run.sh | ( (case x in x) :;; esac)\nbash )', True),
    ('cat /abs/run.sh | echo "$(bash)"', True),
    ('cat /abs/run.sh | x=`bash`', True),
    ('cat /abs/run.sh | while read -r l; do x=$(bash); done', True),
    ('cat /abs/run.sh | case x in x) bash;; esac', True),
    ('cat /abs/run.sh | select y in a; do bash; break; done', True),
    ('cat /abs/run.sh | for i in 1; { bash; }', True),
    ('sudo -Eu nobody python3 -', True),
    ('exec -ca name python3 -', True),
    ('cat /abs/run.sh | { a=()\nbash; }', True),
    ('cat /abs/run.sh | (a=()\nbash)', True),
    ('cat /abs/run.sh | { a=() bash; }', True),
    ('set -- a; cat /abs/run.sh | for i do :; { :; }; bash; break; done', True),
    ('cat /abs/run.sh | for i do bash; done', True),
    ('cat /abs/run.sh | select y do bash; break; done', True),
    ('while true; do function foo { python3 -; }; done', True),
    ('echo ${x:-$(python3 -)}', True),
    ('echo $(( $(python3 -) ))', True),
    ('cat /abs/run.sh | echo ${x:-$(bash)}', True),
    ('echo "${x:-$(python3 -)}"', True),
    ('echo ${x:-`python3 -`}', True),
    ('(( $(python3 -) ))', True),
    ('echo p0wned | tee >(bash)', True),
    ('echo hi > >(bash)', True),
    ('coproc MYPROC { python3 -; }', True),
    ('cat /abs/run.sh | coproc MYPROC { bash; }', True),
    ('cat /abs/a | tee >(sh) >/dev/null', True),
    ('cat /abs/a | coproc MYPROC ( bash )', True),
    ('cat /abs/run.sh | a=() bash', True),
    ('cat /abs/run.sh | a=(1 2) bash', True),
    ('cat /abs/run.sh | a+=(x) bash', True),
    ('cat /abs/run.sh | a[0]=(x) bash', True),
    ('cat /abs/run.sh | (a=() bash)', True),
    ('cat /abs/run.sh | { a=(1 2) bash; }', True),
    ('cat /abs/run.sh | (a=(1 2) bash)', True),
    ('cat /abs/a | a=($(bash))', True),
    ('cat /abs/a | { a=($(bash)); }', True),
    ('cat /abs/a | (a=($(bash)))', True),
    ('cat /abs/a | a=(`bash`)', True),
    ('cat /abs/a | { a=(`bash`); }', True),
    ('cat /abs/a | (a=(`bash`))', True),
    ('cat /abs/a | a+=($(bash))', True),
    ('cat /abs/a | a=(<(bash))', True),
    ('bash ${x:-<(cat /abs/r.sh)}', True),
    ('source ${x:-<(cat /abs/env.sh)}', True),
    ('echo hi | tee ${x:->(bash)}', True),
    ('bash < ${x:-<(cat /abs/r.sh)}', True),
    ('cat /abs/run.sh | { f+x() { bash; }; }', True),
    ('cat /abs/run.sh | a["k"]=1 bash', True),
    ("cat /abs/run.sh | a['k']=1 bash", True),
    ('cat /abs/run.sh | a[\\k]=1 bash', True),
    ('cat /abs/run.sh | a[ 1 ]=1 bash', True),
    ('cat /abs/run.sh | a[;]=1 bash', True),
    ('cat /abs/run.sh | a[ 1 ]=(x) bash', True),
    ('cat /abs/run.sh | a[$i]=1 bash', True),
    ('cat /abs/run.sh | a[$i]=() bash', True),
    ('cat /abs/run.sh | a=1 b[ 2 ]=2 bash', True),
    ('cat /abs/run.sh | 3>/dev/null a[ 1 ]=1 bash', True),
    ('cat /abs/run.sh | { ! a[ 1 ]=1 bash; }', True),
    ('cat /abs/run.sh | while true; do a[ 1 ]=1 bash; break; done', True),
    ('cat /abs/run.sh | a[ $(bash) ]=1', True),
    ('cat /abs/run.sh | (echo a[; bash; ])', True),
    ('cat /abs/run.sh | a=1 time bash', True),
    ('cat /abs/a | { a=(<(bash)); }', True),
    ('cat /abs/a | (a=(<(bash)))', True),
    ('cat /abs/r.sh > ${x:->(bash)}', True),
    ('cat /abs/r.sh | a=(x; bash)', True),
    ("bash -c 'cat /abs/run.sh | bash'", True),
    ("sh -c 'true; echo x | sh'", True),
    ('bash -c "cat /abs/run.sh | python3 -"', True),
    ('bash -c "cat /abs/run.sh | bash"', True),
    ("cat /abs/run.sh | bash -c 'bash'", True),
    ('cat /abs/run.sh | sh -c "true; sh"', True),
    ("bash -c 'bash' <<'EOF'\necho hi\nEOF", True),
    ("zsh -c 'cat /abs/run.sh | zsh'", True),
    ("dash -c 'echo x | dash'", True),
    ("bash -ec 'cat /abs/run.sh | bash'", True),
    ("bash -o pipefail -c 'cat /abs/run.sh | bash'", True),
    ('bash -c "bash -c \'cat /abs/run.sh | bash\'"', True),
    ("sudo -u root bash -c 'cat /abs/run.sh | bash'", True),
    ("cat /abs/run.sh | echo $(bash -c 'bash')", True),
    ('bash -c "cat $f | bash"', True),
    ('cat /abs/run.sh | bash -c "$x; bash"', True),
    ("cat /abs/run.sh | bash -c $'\\x62ash'", True),
    ('cat /abs/run.sh | bash -c {ba,}sh', True),
    ('bash -c <(cat /abs/run.sh)', True),
    ('bash -c \'cat /abs/run.sh | bash "\'', True),
    ('cat <<EOF\n$(cat /abs/run.sh | bash)\nEOF', True),
    ("cat <<EOF\n'$(cat /abs/run.sh | bash)'\nEOF", True),
    ('cat <<EOF\n"$(echo x | sh)"\nEOF', True),
    ('cat <<EOF\n`cat /abs/run.sh | bash`\nEOF', True),
    ('cat <<-EOF\n\t$(cat /abs/run.sh | python3 -)\n\tEOF', True),
    ('cat /abs/run.sh | cat <<EOF\n$(bash)\nEOF', True),
    ("cat /abs/run.sh | cat <<EOF\n'$(bash)'\nEOF", True),
    ('cat <<EOF\n${x:-$(echo x | bash)}\nEOF', True),
    ('cat <<EOF\n$(bash -c "cat /abs/run.sh | bash")\nEOF', True),
    ('cat <<EOF\nplain text\n$(cat /abs/run.sh | sh)\nEOF\necho done', True),
    ('cat <<EOF\n$(cat /abs/run.sh | bash\nEOF', True),
    ("bash -c 'echo $(python3 /abs/s.py)'", True),
    ("bash -c 'echo python3'", True),
    ('bash -c \'echo $"hi"\'', True),
    ("bash -c 'python3'", True),
    ("bash -c 'python3 -'", True),
    ("bash -c 'python3 /dev/stdin'", True),
    ("bash -c 'bash -s'", True),
    ("cat /abs/run.sh | bash -c 'bash >/dev/null'", True),
    ("cat /abs/run.sh | bash -c 'bash # c'", True),
    ("bash -c 'python3 -W ignore'", True),
    ("cat /abs/run.sh | bash -c './sh'", True),
    ("bash -c 'pyth\\\non3 -'", True),
    ("bash -c 'echo hi > >(bash)'", True),
    ("bash -c 'cat /abs/r.sh > ${x:->(bash)}'", True),
    ('bash -c "python3 \'unterminated"', True),
    ("bash -c 'python3 /abs/s.py > /abs/out'", True),
    ('cat <<EOF\n${x python3\nEOF', True),
    ('cat <<EOF\npython3 at ${HOME}\nEOF', True),
    ("bash -c 'cat /abs/run.sh | python3 \"a'", True),
    ('cat <<EOF\n$(echo x | python3 -\nEOF', True),
    ('cat <<EOF\n${x\ncat /abs/run.sh | bash\nEOF', True),
    ('cat <<EOF\n$(cat <<EOF\ncat /abs/run.sh | bash\nEOF)\nEOF', True),
    ('cat <<EOF\n$(cat <<EOF\ncat /abs/run.sh | bash\nEOF\n)\nEOF', True),
    ('cat <<EOF\n`cat <<EOF\ncat /abs/run.sh | bash\nEOF\necho done', True),
    ('cat /abs/run.sh | a[ 1 bash', True),
    ("python3 'unterminated", True),
    ('echo $(python3 -', True),
    ('python3 -I /abs/script.py', False),
    ("python3 -I /abs/script.py <<'EOF'\ndata\nEOF", False),
    ('python3 -I -- /abs/script.py', False),
    ("python3 -I -c 'print(1)'", False),
    ("python3 -Ic 'print(1)'", False),
    ('python3 -m json.tool /abs/x.json', False),
    ('python3 --version', False),
    ('env -i PATH=/usr/bin python3 /abs/script.py', False),
    ('timeout -s KILL 60 python3 -I /abs/script.py', False),
    ('bash /abs/run.sh', False),
    ("bash /abs/run.sh <<'EOF'\ndata\nEOF", False),
    ("bash -c 'echo hi'", False),
    ("printf x | sh -ec 'cat'", False),
    ('bash', False),
    ('bash < /abs/run.sh', False),
    ("perl -e 'print 1'", False),
    ('perl /abs/x.pl', False),
    ("ruby -e 'puts 1'", False),
    ("node -e '1'", False),
    ('node /abs/x.js', False),
    ("php -r 'echo 1;'", False),
    ('php -f /abs/x.php', False),
    ('source /abs/env.sh', False),
    ('. /abs/env.sh', False),
    ("cat <<'EOF'\npython3 -\nbash -s\nEOF", False),
    ("cat > /abs/gen.py <<'EOF'\nimport sys\nEOF", False),
    ('cat <<EOF\nbash -s\nEOF', False),
    ("grep -c x <<<'python3 -'", False),
    ("printf 'x' | wc -c", False),
    ('command -v python3', False),
    ("echo 'python3 - <<EOF'", False),
    ('echo $((1 << 2))', False),
    ('(( x = 1 << 2 ))', False),
    ('diff <(cat /abs/a) <(cat /abs/b)', False),
    ("printf 'x' |\nwc -c", False),
    ('cat /abs/list | while read -r l; do bash /abs/run.sh; done', False),
    ('while true; do bash; break; done', False),
    ('cat /abs/a | while read -r l; do :; done; bash', False),
    ('source -- /abs/env.sh', False),
    ('python3.13t -I /abs/script.py', False),
    ('env -iC /tmp python3 /abs/script.py', False),
    ('cat /abs/a | for i in 1; { :; }; bash', True),
    ('cat /abs/a | case x in x) :;; esac; bash', True),
    ('cat /abs/run.sh | function foo { bash; }', True),
    ('cat /abs/run.sh | foo() { bash; }', True),
    ('sudo -Eu nobody python3 /abs/script.py', False),
    ('cat /abs/a | for x in do; { :; }; bash', True),
    ('cat /abs/run.sh | { foo() { bash; }; }', True),
    ('cat /abs/run.sh | while read -r l; do foo() { bash; }; done', True),
    ('cat /abs/run.sh | if true; then foo() { bash; }; fi', True),
    ('echo ${x:-$(pwd)}', False),
    ('echo $(( $(cat /abs/n) + 1 ))', False),
    ('echo hi | tee >(bash /abs/run.sh)', False),
    ('cat /abs/a | diff <(bash) /abs/b', True),
    ('coproc MYPROC sleep 1', False),
    ('cat /abs/run.sh | a=()\nbash', True),
    ('a=(python3)', False),
    ('{ a=(python3); }', False),
    ('(a=(python3))', False),
    ('a+=(python3 -)', False),
    ('echo hi | tee "${x:->(bash)}"', True),
    ('echo hi | tee ${x:->(bash /abs/run.sh)}', False),
    ('cat /abs/run.sh | a[0]=1 cat', True),
    ('cat /abs/run.sh | a=1 3>/dev/null b[ 2 ]=2 bash', True),
    ('cat /abs/run.sh | a[ 1 ] bash', True),
    ('cat /abs/run.sh | a=(1) while bash', True),
    ('cat /abs/run.sh | a=(1) while bash /abs/run.sh', True),
    ('cat /abs/run.sh | a=1 while bash', True),
    ('cat /abs/run.sh | a=1 until bash', True),
    ('cat /abs/run.sh | a=1 if bash', True),
    ('cat /abs/run.sh | a=1 for bash', True),
    ('cat /abs/run.sh | a=1 case bash', True),
    ('cat /abs/run.sh | a=1 select bash', True),
    ('cat /abs/run.sh | a=1 then bash', True),
    ('cat /abs/run.sh | a=1 do bash', True),
    ('cat /abs/run.sh | a=1 elif bash', True),
    ('cat /abs/run.sh | a=1 else bash', True),
    ('cat /abs/run.sh | a=1 ! bash', True),
    ('cat /abs/run.sh | a=1 coproc bash', True),
    ('cat /abs/run.sh | a=1 function bash', True),
    ('cat /abs/run.sh | a=1 in bash', True),
    ('cat /abs/run.sh | a=1 done bash', True),
    ('cat /abs/run.sh | a=1 fi bash', True),
    ('cat /abs/run.sh | a=1 esac bash', True),
    ('cat /abs/run.sh | a=1 { bash', True),
    ('cat /abs/run.sh | a=1 } bash', True),
    ('cat /abs/run.sh | a=1 [[ bash', True),
    ('cat /abs/run.sh | a=1 ]] bash', True),
    ("cat /abs/run.sh | a=1 'while' bash", True),
    ('cat /abs/run.sh | a[ 1 ]=1 while bash', True),
    ('cat /abs/run.sh | a=1 b=2 until bash', True),
    ('cat /abs/run.sh | a=1 while b=2 bash', True),
    ('cat /abs/run.sh | a=1 ! b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 if b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 then b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 else b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 elif b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 fi b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 case b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 esac b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 for b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 select b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 while b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 until b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 do b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 done b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 in b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 function b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 coproc b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 { b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 } b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 [[ b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 ]] b[ 0 ]=2 bash', True),
    ('cat /abs/run.sh | a=1 while do bash', True),
    ('cat /abs/run.sh | a=1 if env bash', True),
    ('cat /abs/run.sh | { a=1 while bash; }', True),
    ('cat /abs/run.sh | while true; do a=1 for bash; break; done', True),
    ('cat /abs/run.sh | ! a=1 case bash', True),
    ('a=1 while python3 -', True),
    ('a=1 if python3', True),
    ("a=1 until bash <<'EOF'\necho hi\nEOF", True),
    ('a=1 while bash <(cat /abs/run.sh)', True),
    ('cat /abs/run.sh | a=1 while bash /abs/run.sh', True),
    ('cat /abs/run.sh | a=1 while cat', False),
    ('a=1 if python3 -I /abs/script.py', False),
    ('a=1 while bash', False),
    ('cat /abs/run.sh | a=1 while b[ 0 ]=2 bash /abs/run.sh', True),
    ('a=1 while b[ ; cat /abs/run.sh | bash ; ]=2 cat', True),
    ('a=1 while b[ ; python3 - <<<x ; ]=2 cat', True),
    ('a=1 while b[\ncat /abs/run.sh | bash\n]=2 cat', True),
    ('a=1 if b[ && cat /abs/run.sh | bash && ]=2 cat', True),
    ('a=1 ! b[ ; bash <<<x ; ]=2 cat', True),
    ('a=1 do b[ ; bash <(cat /abs/run.sh) ; ]=2 cat', True),
    ("a=1 'while' b[ ; cat /abs/run.sh | bash ; ]=2 cat", True),
    ('a=(1) until b[ ; cat /abs/run.sh | bash ; ]=2 cat', True),
    ('a[ 0 ]=1 in b[ ; cat /abs/run.sh | bash ; ]=2 cat', True),
    ('cat x | a=1 3>out while b[ 0 ]=2 bash', True),
    ('cat x | a=(1) 3>out while b[ 0 ]+=2 python3 -', True),
    ('cat x | a=1 3>out while b[ 0 ]=2 bash /abs/run.sh', True),
    ('echo x > >(a=1 while b[ 0 ]=2 bash)', True),
    ('cat x | a=1 >"$(a=1 while b[ 0 ]=2 bash)" cat', True),
    ('cat x | a=1 >"$(a=1 while bash /abs/run.sh)" cat', True),
    ('cat x | echo "$(echo `a=1 while bash /abs/run.sh`)"', True),
    ("cat x | a=1 $'wh\\x69le' bash", True),
    ("cat x | a=1 $'wh\\x69le' bash /abs/run.sh", True),
    ("cat x | a=1 $'\\167hile' bash /abs/run.sh", True),
    ("cat x | a=1 $'wh\\0zz'ile bash /abs/run.sh", True),
    ('cat x | a=1 $"while" bash /abs/run.sh', True),
    ("cat x | a=1 \"w\"$'\\x68'i\\le bash /abs/run.sh", True),
    ('cat x | time -p a=1 while bash /abs/run.sh', True),
    ('cat x | ! time -p a=(1) until python3 /abs/s.py', True),
    ('cat x | time -- a=1 while bash /abs/run.sh', True),
    ('time -- python3 -', True),
    ('cat /abs/run.sh | time -p -- bash', True),
    ("cat /abs/run.sh | $'\\x62ash'", True),
    ("cat <<$'E\\x4fF'\nhi\nEOF\ncat /abs/run.sh | bash", True),
    ('cat x | a=1 while echo bash', True),
    ('cat /abs/python.log | a=1 while cat', True),
    ("bash -c 'cat /abs/python.log | grep x'", True),
    ('bash -c "echo hi"', False),
    ("bash -c 'python3 /abs/s.py'", False),
    ("bash -c 'cat /abs/run.sh | grep x'", False),
    ('cat /abs/run.sh | bash -c "grep x"', False),
    ("cat /abs/run.sh | bash -c 'bash /abs/run.sh'", False),
    ("bash -c 'bash' < /abs/run.sh", False),
    ('bash -c "echo $HOME"', False),
    ("cat /abs/run.sh | bash -c 'a=1 while bash'", True),
    ("cat <<'EOF'\n$(cat /abs/run.sh | bash)\nEOF", False),
    ('cat <<"EOF"\n$(cat /abs/run.sh | bash)\nEOF', False),
    ('cat <<\\EOF\n$(cat /abs/run.sh | bash)\nEOF', False),
    ('cat <<EOF\n\\$(cat /abs/run.sh | bash)\nEOF', True),
    ('cat <<EOF\n$(python3 /abs/s.py)\nEOF', True),
    ('cat <<EOF\n$(cat /abs/run.sh | grep x)\nEOF', False),
    ("cat <<'EOF'\nbash -c 'cat /abs/run.sh | bash'\nEOF", False),
    ("bash -c 'python3 -I /abs/s.py'", False),
    ("bash -c 'cd /abs && ls .'", False),
    ('cat <<EOF\n$(date)\nEOF', False),
    ('cat <<EOF\npython3 -\nEOF', False),
    ("bash -c 'echo \"a'", False),
    ('cat <<EOF\n$(echo\nEOF', True),
    ('cat <<EOF\n${x\nEOF', True),
    ('cat <<EOF\n$(cat <<EOF\n$(date)\nEOF)\nEOF', True),
    ('cat <<EOF\n$(cat <<EOF\nhi\nEOF\n)\nEOF', False),
    ('cat <<EOF\n`cat <<EOF\nhi\nEOF\necho done', True),
    ('pwd', False),
    ('git add -A', False),
    ('cat /abs/run.sh | bash -ox pipefail', True),
    ('cat /abs/run.sh | bash -xo pipefail', True),
    ('cat /abs/run.sh | bash -oxo pipefail errexit', True),
    ("bash +c 'cat /abs/run.sh | python3 -'", True),
    ("bash +xc 'cat /abs/run.sh | python3 -'", True),
    ("bash +oc pipefail 'cat /abs/run.sh | python3 -'", True),
    ('cat /abs/run.sh | bash +s /abs/x.sh', True),
    ("bash + -c 'cat /abs/run.sh | python3 -'", True),
    ('cat /abs/run.sh | bash +', True),
    ('cat /abs/run.sh | bash + -s', True),
    ('cat /abs/run.sh | dash + -s', True),
    ('bash + /abs/run.sh', False),
    ('bash +x /abs/run.sh', False),
    ('bash +o pipefail /abs/run.sh', False),
    ('bash -ox pipefail -c "cat /abs/run.sh | python3 -"', True),
    ('bash -c "cat /abs/run.sh | python3 -" -ox pipefail', True),
    ('bash -oc pipefail "cat /abs/run.sh | python3 -"', True),
    ('env -Spython3', True),
    ('env --split-string=python3', True),
    ('a=([;]=x)', True),
    ('cat x | time -p a[ 1 ]=1 bash', True),
    ("echo $[ $(printf ']' | wc -c) + 1 ]", True),
    ('bash -c "python3 \'/abs/a b.py\'"', True),
    ("bash -c 'python3 -u /abs/s.py'", True),
    ("bash -c 'bash -x /abs/run.sh'", True),
    ("bash -c $'echo hi'", True),
    ('bash -c "python3 /abs/$f.py"', True),
    ('bash -c "cd $d && ls ."', True),
    ('bash -o pipefail /abs/run.sh', False),
    ('bash -x /abs/run.sh', False),
    ("bash -c 'cat /abs/run.sh | /bin/ba?h'", True),
    ("bash -c 'cat /abs/run.sh | /usr/bin/pyth?n3 -'", True),
    ('cat <<EOF\n$(cat /abs/run.sh | /bin/ba?h)\nEOF', True),
    ("bash -c 'env -Spython3'", False),
    ("bash -c 'env --split-string=python3'", False),
    ("python3 //dev/stdin <<<'print(1)'", True),
    ("python3 /dev/./stdin <<<'print(1)'", True),
    ("python3 /proc/thread-self/fd/0 <<<'print(1)'", True),
    ("bash 00<<<'echo hi'", True),
    ('bash 00< <(cat /abs/run.sh)', True),
    ('exec < <(cat /abs/run.sh); bash', True),
    ('cat /abs/run.sh | sudo -s', False),
    ('cat /abs/run.sh | sudo -i', False),
    ("printf 'echo QA_OK\\n' | a=$'\\c\u00df' bash", True),
    ("printf 'echo QA_OK\\n' | a=$'\\c\ufb00' bash", True),
    ("printf 'echo QA_OK\\n' | a=$'\\c\u0149' bash", True),
    ("echo $'\\q'", False),
    ("cat /abs/run.sh | a=$'\\q' bash", True),
    ("cat /abs/run.sh | a=$'\\d' while bash /abs/run.sh", True),
    ("python3 - $'\\q'", True),
    ("cat x | env $'\\q'=1 bash", True),
    ("cat x | env $'\\d'=1 python3", True),
    ("cat x | env -i $'\\q'=1 bash", True),
    ("cat x | env $'\\x'=1 bash", True),
    ("cat x | env $'\\c'=1 bash", True),
    ("cat x | nohup env $'\\q'=1 bash", True),
    ("cat x | timeout 5 env $'\\q'=1 bash", True),
    ("cat x | sudo $'\\q'=1 bash", True),
    ("cat x | env '\\q'=1 bash", True),
    ('cat x | env a-b=1 bash', True),
    ('cat x | env 1=1 bash', True),
    ("cat x | sudo '\\q'=1 bash", True),
    ('cat x | sudo a-b=1 bash', True),
    ('cat x | sudo 1=1 bash', True),
    ('env a-b=1 python3 /abs/script.py', False),
    ('sudo a-b=1 python3 /abs/script.py', False),
    ('LC_ALL=C grep -rnw in . | head', True),
    ('LC_ALL=C grep -rw "if" . | head', True),
    ('NO_COLOR=1 rg -w done . | head -5', True),
    ('LC_ALL=C find . -name for | sort', True),
    ("printf %s $'\\d'", False),
    ("grep -P $'\\d+\\t' /abs/f", False),
    ("rg $'\\d+\\t' /abs/README.md", False),
    ("sed $'s/\\./,/g' /abs/f", False),
    ('LC_ALL=C grep -rnw in /abs/src | head', False),
    ('grep -rnw in . | head', False),
    ('LC_ALL=C grep -rnw in .', False),
    ("{fd}>o python3 - <<<'print(1)'", True),
    ('cat x | {fd}>/dev/null bash', True),
    ('cat x | {fd}<o bash', True),
    ('cat x | {fd}>o a=1 while bash', True),
    ('cat x | a=1 {fd}>o b=2 bash', True),
    ('cat x | bash {fd}>/dev/null', True),
    ('cat x | {a[1]}>/dev/null bash', True),
    ("cat x | '{fd}'>o bash", True),
    ('cat x | {fd}>/dev/null bash /abs/run.sh', True),
    ("cat x | $'\\x{62}ash'", True),
    ("$'\\x{70}ython3' -", True),
    ("cat x | a=1 $'\\x{77}hile' bash", True),
    ("cat x | a=1 $'\\x{77}hile' python3 /abs/s.py", True),
    ('cat x | /bin/ba?h', True),
    ('cat x | /bin/ba[s]h', True),
    ('cat x | /bin/ba*h', True),
    ('cat x | {,bash}', True),
    ('/usr/bin/pyth?n3 -', True),
    ('{,python3} -', True),
    ("/bin/ba?h <<<'echo hi'", True),
    ('cat x | env /bin/ba?h', True),
    ('cat x | /abs/bin/fil?er', True),
    ('/usr/bin/pyth?n3', True),
    ('/bin/ba?h < /abs/run.sh', True),
    ('cat x | [ -n y ]', False),
    ('cat x | nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup bash', True),
    ('cat x | env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 env a=1 bash', True),
    ("cat x | env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 env a-b=1 bash <<< 'echo 1'", True),
    ('cat x | command command command command command command command command command command command command command command command command command bash', True),
    ('cat x | nice nice nice nice nice nice nice nice nice nice nice nice nice nice nice nice nice bash', True),
    ('cat x | sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo sudo bash', True),
    ("nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup python3 - <<< 'print(1)'", True),
    ('cat x | env "$(printf a=1)" python3', True),
    ('cat x | env $V python3 -', True),
    ('cat x | sudo $(echo a=1) bash', True),
    ('cat x | env $V bash', True),
    ('cat x | $V bash', True),
    ('cat x | a=1 $(true) bash', True),
    ("printf 'echo QA_OK\\n' | env -S $'a-b=1\\_bash'", True),
    ("printf 'echo QA_OK\\n' | env -S $'bash\\_-s'", True),
    ("printf 'echo QA_OK\\n' | env -S $'a=1\\_bash'", True),
    ("cat x | env -S '#x' bash", True),
    ("cat x | env -S '${SHELL}'", True),
    ('cat x | sudo a=1 -u nobody bash', True),
    ('cat x | $PAGER', True),
    ('cat x | sudo -u "$USER" tee /abs/out', True),
    ("cat x | env -S 'grep -e a\\tb'", True),
    ('cat x | sudo a=1 -E tee /abs/out', True),
    ('cat x | sudo -a auth python3 -', True),
    ('cat x | sudo -c class bash', True),
    ('cat x | sudo --user nobody bash', True),
    ('cat x | sudo -z nobody bash', True),
    ('cat x | sudo -Ez nobody bash', True),
    ('cat x | sudo --frobnicate nobody bash', True),
    ('cat x | sudo --log nobody tee /abs/out', True),
    ('cat x | sudo -h bash', True),
    ('cat x | sudo -h host bash', True),
    ('cat x | sudo -h host tee /abs/out', True),
    ('cat x | sudo -Eh host tee /abs/out', True),
    ('cat x | sudo -h', True),
    ('cat x | sudo -hhost bash', True),
    ('cat x | sudo --host=host bash', True),
    ('cat x | sudo --help bash', True),
    ('cat x | sudo --preserve-env=PATH bash', True),
    ('nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup echo hi', True),
    ('cat x | { (( n++ )); bash; }', True),
    ('cat x | while (( 1 )); do bash; done', True),
    ('cat x | while read -r n; do (( $n > 5 )) && bash; done', True),
    ('cat x | (( $(bash) ))', True),
    ('cat x | (( 1 )) bash', True),
    ('cat /abs/run.sh | ((true) && (bash))', True),
    ('cat /abs/run.sh | ((echo hi); (bash))', True),
    ('cat /abs/run.sh | ((:);(bash))', True),
    ('cat /abs/run.sh | ((bash)|(cat))', True),
    ('cat /abs/run.sh | (((:));(bash))', True),
    ('cat /abs/run.sh | if ((:) && (bash)); then :; fi', True),
    ('cat /abs/run.sh | ! ((:) && (bash))', True),
    ('cat /abs/run.sh | time ((:) && (bash))', True),
    ('cat /abs/run.sh | ((:) ; (python3))', True),
    ('cat /abs/run.sh | { ((echo A); (bash)); }', True),
    ('cat /abs/run.sh | while true; do ((echo A); (bash)); break; done', True),
    ('cat /abs/run.sh | coproc ((:) ; (bash))', True),
    ('cat /abs/run.sh | echo $((true) && (bash))', True),
    ('cat /abs/run.sh | echo $((:);(bash))', True),
    ('cat /abs/run.sh | ((echo ")"); (bash))', True),
    ('cat x | /b*/env cat', True),
    ('cat x | /b{in,in}/env cat', True),
    ('cat x | /b*/nohup cat', True),
    ("/b*/env python3 -I /abs/script.py <<< 'x'", True),
    ('/b*/env python3 -I /abs/script.py', True),
    ('/b*/nohup cat', True),
    ('/b*/env bash -c "cat x | bash"', True),
    ('/b{in,in}/env bash -c "cat x | bash"', True),
    ('/usr/bin/[e]nv bash -c "cat x | bash"', True),
    ('e[[:alpha:]]v bash -c "cat x | bash"', True),
    ('e[[=n=]]v bash -c "cat x | bash"', True),
    ('e[[.n.]]v bash -c "cat x | bash"', True),
    ('[[:alpha:]]nv bash -c "cat x | bash"', True),
    ('env -u H* python3 /abs/script.py', True),
    ('timeout 5* python3 /abs/script.py', True),
    ('nohup -{a,b} python3 /abs/script.py', True),
    ('(( $(case x in x) echo 1;; esac) ))', True),
    ('(( $(echo 1 # )\n) ))', True),
    ('cat /abs/run.sh | (( $(while false; do case x in x) :;; esac; done; echo 1) ))', True),
    ('sudo --frobnicate nobody python3 /abs/script.py', True),
    ('sudo --log nobody tee /abs/out', True),
    ('sudo --frobnicate nobody bash -c "cat x | bash"', True),
    ('sudo --log nobody bash -c "cat x | bash"', True),
    ('sudo --us nobody bash -c "cat x | bash"', True),
    ('sudo --us=nobody bash -c "cat x | bash"', True),
    ('cat x | sudo --us nobody bash', True),
    ('cat x | grep bash', False),
    ('echo $V', False),
    ('env a=1 printenv', False),
    ('printf %s "$(date)" | wc -c', False),
    ('cat x | grep "$(date +%Y)"', False),
    ('cat x | env LC_ALL=C sort', False),
    ('cat x | sudo -u nobody tee /abs/out', False),
    ('cat x | sudo --user nobody tee /abs/out', False),
    ('cat x | sudo -hhost tee /abs/out', False),
    ('cat x | sudo --host=host tee /abs/out', False),
    ('cat x | sudo --help tee /abs/out', False),
    ('sudo -h host python3 /abs/script.py', False),
    ('cat x | sudo --preserve-env=PATH tee /abs/out', False),
    ('cat x | sudo -E tee /abs/out', False),
    ('sudo -a auth python3 /abs/script.py', False),
    ("cat x | env -S 'sort -u'", False),
    ('cat x | env LC_ALL=C grep -e "$P"', False),
    ('$V bash', False),
    ('cat x | nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup nohup grep y', False),
    ('cat x | (( 1 ))', False),
    ('git log --oneline | while read -r c; do n=1; (( n++ )); done', False),
    ('cat x | while read -r l; do echo "$l"; (( count++ )); done', False),
    ('cat x | while (( $# )); do shift; done', False),
    ('cat x | { (( $n )); }', False),
    ('cat x | while read -r n; do (( $n > 5 )) && echo big; done', False),
    ('cat x | (( (1) ))', False),
    ('cat x | ((1+(2)))', False),
    ('cat x | (( 16#ff ))', False),
    ('cat x | echo $(( (1) + (2) ))', False),
    ('cat x | if (( (1) )); then :; fi', False),
    ('cat x | sudo --us nobody tee /abs/out', False),
    ('sudo --us nobody python3 /abs/script.py', False),
    ('/usr/bin/pyth?n3 -I /abs/script.py', True),
    ("cat x | grep -e 'a*'", False),
    ('ls *.py | wc -l', False),
    ('cat x | grep -e a*', False),
    ('cat x | env LC_ALL=C grep -e [[:alpha:]]', False),
    ('cat x | tee /abs/{a,b}.out', False),
    ('(( 16#ff + $(echo 1) ))', False),
    ('(( testcase + $(echo 1) ))', False),
    ('(( $(echo 16#ff) ))', False),
    ('(( $(echo testcase) + 1 ))', False),
    ('cat x | (( $(echo case) + 1 ))', True),
    ('cat x | (( $(echo ${#x}) + $# ))', True),
    ('cat /abs/a | diff <($BASH) /abs/b', True),
    ('cat /abs/a | diff <("$BASH") /abs/b', True),
    ('cat /abs/a | diff <($0) /abs/b', True),
    ('cat /abs/a | diff <($SHELL) /abs/b', True),
    ('cat /abs/a | diff <(b${x}ash) /abs/b', True),
    ('cat /abs/a | diff <(${x:-b}ash) /abs/b', True),
    ('cat /abs/a | diff <(py${x}thon3) /abs/b', True),
    ('cat /abs/a | diff <(env $BASH) /abs/b', True),
    ('cat /abs/a | cat <($BASH)', True),
    ('$BASH 00< <(cat /abs/run.sh)', True),
    ('b${x}ash 00< <(cat /abs/run.sh)', True),
    ('exec < <(cat /abs/run.sh); $BASH', True),
    ('cat x | eval b${x}ash', True),
]


def self_test() -> int:
    bad = 0
    for command, should_block in SELF_TEST:
        problem = decide(command)
        got = problem is not None
        if got != should_block:
            bad += 1
            print("FAIL want=" + ("BLOCK" if should_block else "allow") + " got="
                  + ("BLOCK" if got else "allow") + ": " + repr(command))
            continue
        if got:
            message = render(problem)
            if any(message.count(marker) != 1 for marker in
                   ("BLOCKED (stdin-interpreter): ", "\nWHY: ", "\nCONSIDER INSTEAD: write ")):
                bad += 1
                print("FAIL message contract: " + repr(command))
    print(str(len(SELF_TEST) - bad) + "/" + str(len(SELF_TEST)) + " self-test cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
