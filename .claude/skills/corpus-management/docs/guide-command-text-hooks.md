# Command-text hooks and declared staged paths

**Document Title:** Command-text hooks and declared staged paths\
**Document Type:** Guide\
**Version:** 1.0.6\
**Date:** 2026-11-24\
**Owner:** Governance Library Maintainer\
**Approving Authority:** Governance Library Maintainer\
**Related Documents:** [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md)\
**Classification:** Public\
**Category:** Documentation\
**Review Frequency:** Upon material change to the commit workflow\
**Repository Path:** [`.claude/skills/corpus-management/docs/guide-command-text-hooks.md`](guide-command-text-hooks.md)\
**Confidentiality:** Public\
**License:** CC BY-SA 4.0

---

## Purpose and scope

This guide explains the coverage and limits of the command-text hooks and the
independent staged-path check. It covers hook installation, explicit path
declarations, and the checks and limitations that apply to the commit workflow.

The Bash hooks read `tool_input.command`. Commands inside a script file, a heredoc
fed to a shell, or a subprocess are not generally visible. Recognizing selected
shell strings or heredoc forms does not provide recursive execution inspection.
The bulk-add parser already detects some literal Git commands in shell heredocs;
that partial handling does not extend to a script invoked by the heredoc.
These are workflow guards, not an execution or authorization boundary.
The shared command-word helper skips leading assignments, known wrapper names,
option-looking words and numeric durations. It does not know which wrapper
options consume values: for example, it reads `timeout -s KILL 5 git add -A`
as starting with `KILL`. Unsupported prefixes and dynamic program words are not
generally rejected. The bulk-add hook splits command text at separators and
inspects recognized Git invocations and selected shell strings with a separate
`-c` argument. This is not a shell parser; quoted separators, shell option bundles,
reserved words, aliases and shell functions can affect what it recognizes.
A tokenization failure can leave a segment uninspected.

The leading `GRC_ALLOW_BULK_ADD=1` escape is checked after heredoc readability.
An unreadable heredoc is refused, including the escape, when a raw word could be
Git. Without such a word, the bulk-add hook allows the unreadable command; it
does not separately reject dynamic program prefixes. The verification-pipe hook
also checks selected raw-text patterns, while the stdin-interpreter hook uses
its own reader. These checks do not establish general execution coverage.

| Hook | Command-text residual |
| --- | --- |
| `block-bulk-git-add.py` | Script files, shell heredocs and subprocess staging can escape detection. It also accepts directory operands, so enumeration alone does not establish a file set. |
| `block-unbumped-version-commit.py` | A commit inside a script file, shell heredoc or subprocess may never trigger the staged Version check. Its recognized command text does not prove that every commit was inspected. |
| `block-verification-pipes.py` | Pipelines inside script files, shell heredocs or subprocesses are not generally inspected. Selected raw-text matches can still refuse heredoc text; this is not general execution coverage. |
| `block-stdin-interpreter.py` | Recognized interpreter stdin feeds are refused, but commands inside script files, shell heredocs or subprocesses are not generally inspected. Its partial heredoc handling does not establish what a child executes. |
| `block-repeated-tool-failure.py` | It compares submitted command strings and recorded blocks. Changed wrappers can hide the same failing command inside a script file, shell heredoc or subprocess. |

`block-branch-to-main-edit.py` reads an Edit/Write file path, not Bash command text;
it is outside this list. The helpers `_hookutil.py` and `_hook_state.py` are not hooks.

## Independent staging check

The native [pre-commit chain](../tools/git-hooks/pre-commit) runs
[check-staged-paths.py](../tools/check-staged-paths.py) after the branch,
generated-output and CHANGELOG checks. The existing installed dispatcher resolves
the active checkout on every invocation, so it needs no update. To install it in
a new clone, run `sh .claude/skills/corpus-management/tools/install-git-hooks.sh`.
When also using the pre-commit framework, install the native hooks first, then run
`pre-commit install`, which chains the native dispatcher as `pre-commit.legacy`.
A foreign existing hook must be integrated as the installer explains.

From the repository root, explicitly declare the complete intended set:

```sh
python3 -I .claude/skills/corpus-management/tools/check-staged-paths.py --declare -- README.md governance/policy.md
git add -- README.md governance/policy.md
python3 -I .claude/skills/corpus-management/tools/check-staged-paths.py --pre-commit
```

The command writes `grc-staged-paths.json` inside the directory returned by
`git rev-parse --absolute-git-dir`. This is local Git metadata, never a tracked
file, and each linked worktree has its own declaration. Its JSON object contains
`head` (the current commit hash, or null on an unborn branch) and `paths` (a list
of literal repository-relative file names). The declaration command never reads
the staged path set or stages files. Review the intended scope before declaring;
do not generate the declaration from the index to rubber-stamp a sweep.

Paths are exact, case-sensitive names, not pathspecs: list every file, including
generated outputs, both names of a rename, and deleted paths. Quote spaces and
shell metacharacters. Directories and wildcard expressions do not expand in the
checker. Duplicate entries, absolute paths and noncanonical components are
invalid. `--declare --` explicitly declares an empty staged diff. Re-declare to
change scope, or after HEAD changes; the declaration otherwise remains available
for retries. Removing it makes the next check refuse.

The check compares sets using NUL-delimited Git output with rename detection
disabled. It preserves `GIT_INDEX_FILE`, so it inspects the index Git intends to
commit, including temporary indexes for partial or all-tracked commits. It
refuses missing, malformed or stale declarations, unreadable state, unresolved
merge entries, and either direction of mismatch. Diagnostics distinguish
undeclared staged paths from declared paths not staged and show how to declare.
There is no environment opt-out. A missing checker also fails the tracked chain.

## Remaining limits and validation

Every staging route produces an index that this check can inspect when the
native pre-commit hook runs: direct Git, script files, shell heredocs and child
processes. The check does not intercept staging itself. It establishes only path
set equality at inspection time, not content approval, message accuracy or author
intent. An author can edit the declaration, checker or hooks. Concurrent index
changes or later hooks that modify the index after inspection remain a race. Amend is measured against HEAD, not the
amended commit's parent. Submodules are represented by their gitlink paths, not
by paths in their own repositories.

No local hook covers uninstalled or deliberately skipped hooks, an older checkout
without this chain, or operations that do not invoke pre-commit, such as clean
merges and sequencer-generated commits. Those remain outside this backstop.

The focused regression class `DeclaredStagedPathsTests` runs through real Git
indexes and directly invokes the native hook without creating commits. It tests
script, heredoc and subprocess staging, missing/malformed declarations, exact
sets, extra/missing paths, special file names, effective-index selection and
fail-closed wiring. Separate mutations that disable set comparison or allow a
missing declaration are detected by the focused tests. Its flips show a permitted set becoming refused after scope
changes and becoming permitted again only after an explicit corrected declaration.
Full-suite validation also covers the existing commit-creating fixtures.
